import tensorflow as tf

import numpy as np
class GHM_Loss:
    def __init__(self, bins=10, momentum=0.75):
        self.g =None
        self.avg = 0
        self.bins = bins
        self.mu = 0.02
        self.momentum = momentum
        self.valid_bins = tf.constant(0.0, dtype=tf.float32)
        self.edges_left, self.edges_right = self.get_edges(self.bins)
        if momentum > 0:
            acc_sum = [0.0 for _ in range(bins)]
            self.acc_sum = tf.Variable(acc_sum, trainable=False)

    @staticmethod
    def get_edges(bins):
        edges_left = [float(x) / bins for x in range(bins)]
        edges_left = tf.constant(edges_left)  # [bins]
        edges_left = tf.expand_dims(edges_left, -1)  # [bins, 1]
        edges_left = tf.expand_dims(edges_left, -1)  # [bins, 1, 1]
        edges_left = tf.expand_dims(edges_left, -1)  # [bins, 1, 1, 1]
        edges_left = tf.expand_dims(edges_left, -1)  # [bins, 1, 1, 1, 1]

        edges_right = [float(x) / bins for x in range(1, bins + 1)]
        edges_right[-1] += 1e-3
        edges_right = tf.constant(edges_right)  # [bins]
        edges_right = tf.expand_dims(edges_right, -1)  # [bins, 1]
        edges_right = tf.expand_dims(edges_right, -1)  # [bins, 1, 1]
        edges_right = tf.expand_dims(edges_right, -1)  # [bins, 1, 1, 1]
        edges_right = tf.expand_dims(edges_right, -1)  # [bins, 1, 1, 1, 1]

        return edges_left, edges_right


    def calc(self, g, valid_mask):
        edges_left, edges_right = self.edges_left, self.edges_right
        alpha = self.momentum
        # valid_mask = tf.cast(valid_mask, dtype=tf.bool)

        tot = tf.maximum(tf.reduce_sum(tf.cast(valid_mask, dtype=tf.float32)), 1.0)


        inds_mask = tf.logical_and(tf.greater_equal(g, edges_left), tf.less(g, edges_right))

        zero_matrix = tf.cast(tf.zeros_like(inds_mask), dtype=tf.float32)  # [bins, batch_num, class_num]

        inds = tf.cast(tf.logical_and(inds_mask, valid_mask), dtype=tf.float32)  # [bins, batch_num, class_num]

        num_in_bin = tf.reduce_sum(inds, axis=[1, 2, 3, 4])  # [bins] according to batch

        valid_bins = tf.greater(num_in_bin, 0)  # [bins]

        num_valid_bin = tf.reduce_sum(tf.cast(valid_bins, dtype=tf.float32))

        if alpha > 0:
            update = tf.assign(self.acc_sum,
                               tf.where(valid_bins, alpha * self.acc_sum + (1 - alpha) * num_in_bin, self.acc_sum))
            with tf.control_dependencies([update]):
                acc_sum_tmp = tf.identity(self.acc_sum, name='updated_accsum')
                acc_sum = tf.expand_dims(acc_sum_tmp, -1)  # [bins, 1]
                acc_sum = tf.expand_dims(acc_sum, -1)  # [bins, 1, 1]
                acc_sum = tf.expand_dims(acc_sum, -1)  # [bins, 1, 1, 1]
                acc_sum = tf.expand_dims(acc_sum, -1)  # [bins, 1, 1, 1 , 1]

                acc_sum = acc_sum + zero_matrix  # [bins, batch_num, class_num]
                weights = tf.where(tf.equal(inds, 1), tot / acc_sum, zero_matrix)
                weights = tf.reduce_sum(weights, axis=0)

        else:
            num_in_bin = tf.expand_dims(num_in_bin, -1)  # [bins, 1]
            num_in_bin = tf.expand_dims(num_in_bin, -1)  # [bins, 1, 1]
            num_in_bin = tf.expand_dims(num_in_bin, -1)  # [bins, 1, 1, 1]
            num_in_bin = tf.expand_dims(num_in_bin, -1)  # [bins, 1, 1, 1, 1]

            num_in_bin = num_in_bin + zero_matrix  # [bins, batch_num, class_num]
            weights = tf.where(tf.equal(inds, 1), tot / num_in_bin, zero_matrix)

            weights = tf.reduce_sum(weights, axis=0)

        weights = weights / num_valid_bin


        return weights, tot

    def ghm_class_loss(self, logits, targets, masks=None):
        """ Args:
        input [batch_num, class_num]:
            The direct prediction of classification fc layer.
        target [batch_num, class_num]:
            Binary target (0 or 1) for each sample each class. The value is -1
            when the sample is ignored.
        """
        train_mask = (1 - tf.cast(tf.equal(targets, -1), dtype=tf.float32))
        self.g = tf.abs(tf.sigmoid(logits) - targets) # [batch_num, class_num]
        g = tf.expand_dims(self.g, axis=0)  # [1, batch_num, class_num]

        if masks is None:
            masks = tf.ones_like(targets)
        valid_mask = masks > 0
        weights, tot = self.calc(g, valid_mask)
        print(weights.shape)
        ghm_class_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=targets*train_mask,
                                                                 logits=logits)
        ghm_class_loss = tf.reduce_sum(ghm_class_loss * weights) / tot

        return ghm_class_loss


    def ghm_regression_loss(self, logits, targets, masks):
        """ Args:
        input [batch_num, *(* class_num)]:
            The prediction of box regression layer. Channel number can be 4 or
            (4 * class_num) depending on whether it is class-agnostic.
        target [batch_num,  *(* class_num)]:
            The target regression values with the same size of input.
        """
        mu = self.mu

        # ASL1 loss
        diff = logits - targets
        # gradient length
        g = tf.abs(diff / tf.sqrt(mu * mu + diff * diff))

        if masks is None:
            masks = tf.ones_like(targets)
        valid_mask = masks > 0

        weights, tot = self.calc(g, valid_mask)

        ghm_reg_loss = tf.sqrt(diff * diff + mu * mu) - mu

        ghm_reg_loss = tf.reduce_sum(ghm_reg_loss * weights,axis=-1,keep_dims=True) #/ tot

        return ghm_reg_loss#,weights

class GHM_Loss2:
    def __init__(self, bins=10, momentum=0.75):
        self.g = None
        self.bins = bins
        self.momentum = momentum
        self.valid_bins = tf.constant(0.0, dtype=tf.float32)
        self.edges_left, self.edges_right = self.get_edges(self.bins)
        if momentum > 0:
            acc_sum = [0.0 for _ in range(bins)]
            self.acc_sum = tf.Variable(acc_sum, trainable=False)

    @staticmethod
    def get_edges(bins):
        edges_left = [float(x) / bins for x in range(bins)]
        edges_left = tf.constant(edges_left) # [bins]
        edges_left = tf.expand_dims(edges_left, -1) # [bins, 1]
        edges_left = tf.expand_dims(edges_left, -1) # [bins, 1, 1]

        edges_right = [float(x) / bins for x in range(1, bins + 1)]
        edges_right[-1] += 1e-6
        edges_right = tf.constant(edges_right) # [bins]
        edges_right = tf.expand_dims(edges_right, -1) # [bins, 1]
        edges_right = tf.expand_dims(edges_right, -1) # [bins, 1, 1]
        return edges_left, edges_right


    def calc(self, g, valid_mask):
        edges_left, edges_right = self.edges_left, self.edges_right
        alpha = self.momentum
        # valid_mask = tf.cast(valid_mask, dtype=tf.bool)

        tot = tf.maximum(tf.reduce_sum(tf.cast(valid_mask, dtype=tf.float32)), 1.0)
        inds_mask = tf.logical_and(tf.greater_equal(g, edges_left), tf.less(g, edges_right))
        zero_matrix = tf.cast(tf.zeros_like(inds_mask), dtype=tf.float32)  # [bins, batch_num, class_num]

        inds = tf.cast(tf.logical_and(inds_mask, valid_mask), dtype=tf.float32)  # [bins, batch_num, class_num]

        num_in_bin = tf.reduce_sum(inds, axis=[1, 2])  # [bins]
        valid_bins = tf.greater(num_in_bin, 0)  # [bins]

        num_valid_bin = tf.reduce_sum(tf.cast(valid_bins, dtype=tf.float32))

        if alpha > 0:
            update = tf.assign(self.acc_sum,
                               tf.where(valid_bins, alpha * self.acc_sum + (1 - alpha) * num_in_bin, self.acc_sum))
            with tf.control_dependencies([update]):
                acc_sum_tmp = tf.identity(self.acc_sum, name='updated_accsum')
                acc_sum = tf.expand_dims(acc_sum_tmp, -1)  # [bins, 1]
                acc_sum = tf.expand_dims(acc_sum, -1)  # [bins, 1, 1]
                acc_sum = acc_sum + zero_matrix  # [bins, batch_num, class_num]
                weights = tf.where(tf.equal(inds, 1), tot / acc_sum, zero_matrix)
                weights = tf.reduce_sum(weights, axis=0)

        else:
            num_in_bin = tf.expand_dims(num_in_bin, -1)  # [bins, 1]
            num_in_bin = tf.expand_dims(num_in_bin, -1)  # [bins, 1, 1]
            num_in_bin = num_in_bin + zero_matrix  # [bins, batch_num, class_num]
            weights = tf.where(tf.equal(inds, 1), tot / num_in_bin, zero_matrix)
            weights = tf.reduce_sum(weights, axis=0)

        weights = weights / num_valid_bin

        return weights, tot


    def ghm_class_loss(self, logits, targets, masks=None):
        """ Args:
        input [batch_num, class_num]:
            The direct prediction of classification fc layer.
        target [batch_num, class_num]:
            Binary target (0 or 1) for each sample each class. The value is -1
            when the sample is ignored.
        """
        train_mask = (1 - tf.cast(tf.equal(targets, -1), dtype=tf.float32))
        self.g = tf.abs(tf.sigmoid(logits) - targets) # [batch_num, class_num]
        g = tf.expand_dims(self.g, axis=0)  # [1, batch_num, class_num]

        if masks is None:
            masks = tf.ones_like(targets)
        valid_mask = masks > 0
        weights, tot = self.calc(g, valid_mask)
        print(weights.shape)
        ghm_class_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=targets*train_mask,
                                                                 logits=logits)
        ghm_class_loss = tf.reduce_sum(ghm_class_loss * weights) / tot

        return ghm_class_loss


    def ghm_regression_loss(self, logits, targets, masks):
        """ Args:
        input [batch_num, *(* class_num)]:
            The prediction of box regression layer. Channel number can be 4 or
            (4 * class_num) depending on whether it is class-agnostic.
        target [batch_num,  *(* class_num)]:
            The target regression values with the same size of input.
        """
        mu = self.mu

        # ASL1 loss
        diff = logits - targets
        # gradient length
        g = tf.abs(diff / tf.sqrt(mu * mu + diff * diff))

        if masks is None:
            masks = tf.ones_like(targets)
        valid_mask = masks > 0

        weights, tot = self.calc(g, valid_mask)

        ghm_reg_loss = tf.sqrt(diff * diff + mu * mu) - mu
        ghm_reg_loss = tf.reduce_sum(ghm_reg_loss * weights) / tot

        return ghm_reg_loss

'''
if __name__ == '__main__':

    ghm = GHM_Loss(momentum=0.75)
    input_1 = tf.constant([[[0.025, 0.35], [0.45, 0.85]]], dtype=tf.float32)
    target_1 = tf.constant([[[1.0, 1.0], [0.0, 1.0]]], dtype=tf.float32)

    input_2 = tf.Variable(tf.random_uniform([2,2,4,8]), dtype=tf.float32)
    target_2 = tf.Variable(tf.random_uniform([2,2,4,8]), dtype=tf.float32)
    print(input_1.shape)
    mask = tf.ones_like(target_2)


    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        loss,weights = ghm.ghm_regression_loss(input_2, target_2,mask)

        print(sess.run([loss,ghm.acc_sum,weights]))#
        #print(sess.run([ghm.acc_sum]))

        loss ,weights = ghm.ghm_regression_loss(input_2, target_2,mask)
        print(sess.run([loss,ghm.acc_sum,weights]))

        loss = ghm.ghm_class_loss(input_2, target_2)
        print(sess.run([loss, ghm.g, ghm.acc_sum]))
        loss = ghm.ghm_class_loss(input_1, target_1)
        print(sess.run([loss, ghm.g, ghm.acc_sum]))
        loss = ghm.ghm_class_loss(input_1, target_1)
        print(sess.run([loss, ghm.g, ghm.acc_sum]))
        loss = ghm.ghm_class_loss(input_1, target_1)
        print(sess.run([loss, ghm.g, ghm.acc_sum]))
'''

import cv2
import os
# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="page_tflite_1221.tflite")#"model512.tflite"
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def padding_resize(image):
    h ,w ,_ = image.shape

    if w > h:
        ww = int(0.1 *w)
        left = int(0.05 *w)
        right = ww - left

        up = (w + ww - h )// 2
        down = w + ww - h - up

        image = cv2.copyMakeBorder(image, up, down, left, right, cv2.BORDER_CONSTANT, value=[128, 128, 128])
        image = cv2.resize(image, (512, 512))
        scale = (w + ww) / 512

    else:
        left = (h - w) // 2
        right = (h - w) - left
        up = 0
        down = 0

        image = cv2.copyMakeBorder(image, up, down, left, right, cv2.BORDER_CONSTANT, value=[128, 128, 128])#value=[0, 0, 0]
        image = cv2.resize(image, (512, 512))
        scale = h / 512.0

    return image,left,up,scale

def padding_resize_hand(image):
    h, w, _ = image.shape
    if w > h:
        left = 0
        right = 0

        up = (w - h) // 2
        down = w - h - up

        image = cv2.copyMakeBorder(image, up, down, left, right, cv2.BORDER_CONSTANT, value=[128, 128, 128])
        image = cv2.resize(image, (320, 320))
        scale = w / 320
    else:
        left = (h - w) // 2
        right = (h - w) - left
        up = 0
        down = 0

        image = cv2.copyMakeBorder(image, up, down, left, right, cv2.BORDER_CONSTANT, value=[128, 128, 128])
        image = cv2.resize(image, (320, 320))
        scale = h / 320
    return image,left,up,scale

def page_detect(input_image):
    h,w,_ = input_image.shape
    im = cv2.cvtColor(input_image,cv2.COLOR_BGR2RGB)

    img, left,up,scale = padding_resize(im)

    img = np.array(img,dtype=np.float32)

    #print(img.shape)
    image_np_expanded = 2.0*(np.expand_dims(img, axis=0) / 255.0) - 1.0#/ 256.0

    interpreter.set_tensor(input_details[0]['index'], image_np_expanded)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    output_data = np.squeeze(output_data)

    score_map = np.multiply(output_data[:, :, 0], output_data[:, :, 1])  # output_data[:,:,1]#

    xy_text = np.where(score_map == np.max(score_map))
    print(np.max(score_map))
    if np.max(score_map) < 0.67:
        return False,None

    poly = [512.0 * i for i in output_data[xy_text[0][0], xy_text[1][0], 2:]]

    poly_list = [xy_text[1][0] * 4 - poly[6], xy_text[0][0] * 4 - poly[7], xy_text[1][0] * 4 + poly[0],
                 xy_text[0][0] * 4 - poly[1], xy_text[1][0] * 4 + poly[2],
                 xy_text[0][0] * 4 + poly[3], xy_text[1][0] * 4 - poly[4], xy_text[0][0] * 4 + poly[5]]

    ########
    poly_list_input_image = [poly_list[0]*scale - left, poly_list[1]*scale - up, poly_list[2]*scale - left, poly_list[3]*scale - up,poly_list[4]*scale - left, poly_list[5]*scale - up,poly_list[6]*scale - left, poly_list[7]*scale - up ]

    #pt = np.array(poly_list_input_image, np.int32)
    #pt = np.array(poly_list, np.int32)

    #pt = pt.reshape((-1, 1, 2))

    #print(pt)
    #cv2.polylines(img, [pt], True, (255, 0, 255))
    #cv2.polylines(input_image, [pt], True, (255, 0, 255))
    #cv2.circle(input_image, (int(4 * xy_text[1][0]*scale - left ), int(4 * xy_text[0][0] * scale - up)), 10, (0, 0, 255), 5)
    #cv2.circle(img, (int(4 * xy_text[1][0] ), int(4 * xy_text[0][0])), 10, (0, 0, 255), 5)
    #points = []
    x1 = poly_list_input_image[0]
    if x1< 0:
        x1=0

    y1 = poly_list_input_image[1]
    if y1< 0:
        y1=0

    x2 = poly_list_input_image[2]
    if x2 > w:
        x2=w-1

    y2 = poly_list_input_image[3]
    if y2 < 0:
        y2=0

    x3 = poly_list_input_image[4]
    if x3 > w:
        x3=w-1

    y3 = poly_list_input_image[5]
    if y3 > h:
        y3=h-1

    x4 = poly_list_input_image[6]
    if x4 < 0:
        x4 =0

    y4 = poly_list_input_image[7]
    if y4 > h:
        y4=h-1

    return_points = [x1,y1,x2,y2,x3,y3,x4,y4]
    return True,return_points

#'''
interpreter_hand = tf.lite.Interpreter(model_path="output_detect.tflite")#"model512.tflite"
interpreter_hand.allocate_tensors()

# Get input and output tensors.
input_details_hand = interpreter_hand.get_input_details()
output_details_hand = interpreter_hand.get_output_details()
#'''
def hand_detect(input_image):
    h,w,_ = input_image.shape
    im,left,up,scale = padding_resize_hand(input_image.copy())
    image_np = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    image_np_expanded = 2.0*(np.expand_dims(image_np, axis=0) / 255.0) - 1.0#/ 256.0
    image_np_expanded = image_np_expanded.astype('float32')

    #print(image_np_expanded.shape)
    interpreter_hand.set_tensor(input_details_hand[0]['index'], image_np_expanded)
    interpreter_hand.invoke()

    boxes = interpreter_hand.get_tensor(output_details_hand[0]['index'])

    scores = interpreter_hand.get_tensor(output_details_hand [2]['index'])

    #print(boxes[0][1])
    #print(scores[0])

    if scores[0][0] < 0.95:
        return False,None
    #print(scores[0][0])
    # print(boxes[0][0])
    xmin = int(boxes[0][0][1] * 320)
    ymin = int(boxes[0][0][0] * 320)

    xmax = int(boxes[0][0][3] * 320)
    ymax = int(boxes[0][0][2] * 320)
    #points = [xmin * scale - left, ymin * scale - up, xmax * scale - left, ymax * scale - up]

    minx = xmin * scale- left
    if minx < 0:
        minx=0

    miny = ymin * scale - up
    if miny < 0:
        miny=0

    maxx = xmax * scale - left
    if maxx > w:
        maxx= w-1

    maxy = ymax * scale - up
    if maxy >h :
        maxy=h-1

    return_points = [minx,miny,maxx,maxy]

    if scores[0][1] < 0.95:
        #cv2.rectangle(input_image, (int(points[0]), int(points[1])), (int(points[2]), int(points[3])), (255, 0, 255), 5)
        return True,return_points

    #cv2.rectangle(input_image, (int(points[0]), int(points[1])), (int(points[2]), int(points[3])), (255, 0, 255), 5)
    xmin = int(boxes[0][1][1] * 320)
    ymin = int(boxes[0][1][0] * 320)

    xmax = int(boxes[0][1][3] * 320)
    ymax = int(boxes[0][1][2] * 320)

    #points.extend([xmin * scale - left, ymin * scale - up, xmax * scale - left, ymax * scale - up])

    minx = xmin * scale- left
    if minx < 0:
        minx=0

    miny = ymin * scale - up
    if miny < 0:
        miny=0

    maxx = xmax * scale - left
    if maxx > w:
        maxx= w-1

    maxy = ymax * scale - up
    if maxy >h :
        maxy=h-1

    return_points.extend([minx, miny, maxx, maxy])
    #image_np = cv2.cvtColor(image_np.copy(), cv2.COLOR_RGB2BGR)
    #cv2.rectangle(input_image, (int(points[4]), int(points[5])), (int(points[6]), int(points[7])), (255, 0, 255), 5)
    #print(points)


    return True,return_points

import shapely
from shapely.geometry import Polygon
def Cal_area_2poly(data1,data2):

    poly1 = Polygon(data1).convex_hull
    poly2 = Polygon(data2).convex_hull

    if not poly1.intersects(poly2):
        inter_area = 0
    else:
        inter_area = poly1.intersection(poly2).area
    return inter_area


def is_hand_cover(page_points,hand_points):
    if len(hand_points) == 4:
        hand_area = (hand_points[2] - hand_points[0]) * (hand_points[3] - hand_points[1])

        page = np.array(page_points).reshape(4, 2)

        hand = [hand_points[0],hand_points[1],hand_points[2],hand_points[1],hand_points[2],hand_points[3],hand_points[0],hand_points[3]]
        hand = np.array(hand).reshape(4, 2)

        insec_area = Cal_area_2poly(page,hand)
        if insec_area / hand_area > 0.1:
            return True
        else:
            return False


    if len(hand_points) == 8:
        hand_area1 = (hand_points[2] - hand_points[0]) * (hand_points[3] - hand_points[1])
        hand_area2 = (hand_points[6] - hand_points[4]) * (hand_points[7] - hand_points[5])


        page = np.array(page_points).reshape(4, 2)

        hand1 =  [hand_points[0],hand_points[1],hand_points[2],hand_points[1],hand_points[2],hand_points[3],hand_points[0],hand_points[3]]
        hand1 = np.array(hand1).reshape(4, 2)

        insec_area1 = Cal_area_2poly(page,hand1)

        hand2 =  [hand_points[4],hand_points[5],hand_points[6],hand_points[5],hand_points[6],hand_points[7],hand_points[4],hand_points[7]]
        hand2 = np.array(hand2).reshape(4, 2)
        insec_area2 = Cal_area_2poly(page,hand2)

        if insec_area1 / hand_area1 > 0.1 or insec_area2 / hand_area2 > 0.1:
            return True
        else:
            return False



def page_hand_detect(input_image):
    input_image = cv2.flip(input_image, 1)
    is_page,page_points = page_detect(input_image.copy())
    is_hand,hand_points = hand_detect(input_image.copy())

    if is_page == False:
        return -1,input_image
    else:
        if is_hand == False:
            pt = np.array(page_points, np.int32)
            pt = pt.reshape((-1, 1, 2))
            cv2.polylines(input_image, [pt], True, (255, 0, 255))
            return 0,input_image
        else:
            pt = np.array(page_points, np.int32)
            pt = pt.reshape((-1, 1, 2))
            cv2.polylines(input_image, [pt], True, (255, 0, 255),thickness=5)

            is_cover = is_hand_cover(page_points,hand_points)

            if is_cover == False:
                return 1,input_image

            if len(hand_points)==4:
                cv2.rectangle(input_image, (int(hand_points[0]), int(hand_points[1])), (int(hand_points[2]), int(hand_points[3])),
                              (255, 0, 255), 5)
            else:
                cv2.rectangle(input_image, (int(hand_points[0]), int(hand_points[1])), (int(hand_points[2]), int(hand_points[3])),
                              (255, 0, 255), 5)
                cv2.rectangle(input_image, (int(hand_points[4]), int(hand_points[5])), (int(hand_points[6]), int(hand_points[7])),
                              (255, 0, 255), 5)

            return 2,input_image




#image = cv2.imread('page_coverIMG_20201126_095515_465.jpg')#page_coverIMG_20201126_162815_140
image = cv2.imread('page_coverIMG_20201126_162815_140.jpg')
#image = cv2.flip(image, 1)
#img,_,_ = hand_detect(image)
flag,img = page_hand_detect(image)
cv2.imwrite('test.jpg',img)
print(flag)