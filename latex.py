import importlib
import random
import sys
importlib.reload(sys)
import requests
import lxml.etree as etree
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

SVG = [
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_1_binary_plus.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_2_binary_minus.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_3_binary_times.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_4_binary_div.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_5_binary_pm.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_6_binary_mp.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_7_binary_triangleleft.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_8_binary_triangleright.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_9_binary_cdot.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_10_binary_setminus.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_11_binary_star.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_12_binary_ast.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_13_binary_cup.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_14_binary_cap.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_15_binary_sqcup.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_16_binary_sqcap.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_17_binary_vee.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_18_binary_wedge.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_19_binary_circ.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_20_binary_bullet.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_21_binary_oplus.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_22_binary_ominus.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_23_binary_odot.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_24_binary_oslash.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_25_binary_otimes.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_26_binary_bigcirc.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_27_binary_diamonda.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_28_binary_uplus.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_29_binary_bigtriangleup.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_30_binary_bigtriangledown.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_31_binary_lhd.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_32_binary_rhd.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_33_binary_unlhd.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_34_binary_unrhd.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_35_binary_amalg.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_36_binary_wr.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_37_binary_dagger.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_38_binary_ddagger.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_39_relation_less.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_40_relation_more.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_41_relation_equal.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_42_relation_le.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_43_relation_ge.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_44_relation_equiv.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_45_relation_ll.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_46_relation_gg.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_47_relation_doteq.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_48_relation_prec.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_49_relation_succ.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_50_relation_sim.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_51_relation_preceq.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_52_relation_succeq.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_53_relation_simeq.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_54_relation_approx.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_55_relation_subset.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_56_relation_supset.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_57_relation_subseteq.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_58_relation_supseteq.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_59_relation_sqsubset.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_60_relation_sqsupset.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_61_relation_sqsubseteq.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_62_relation_sqsupseteq.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_63_relation_cong.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_64_relation_Join.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_65_relation_bowtie.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_66_relation_propto.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_67_relation_in.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_68_relation_ni.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_69_relation_vdash.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_70_relation_dashv.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_71_relation_models.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_72_relation_mid.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_73_relation_parallel.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_74_relation_perp.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_75_relation_smile.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_76_relation_frown.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_77_relation_asymp.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_78_relation_slash.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_79_relation_notin.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_80_relation_ne.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_81_arrow_gets.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_82_arrow_to.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_83_arrow_longleftarrowa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_84_arrow_longrightarrowa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_85_arrow_uparrowa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_86_arrow_downarrowa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_87_arrow_updownarrowa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_88_arrow_leftrightarrowa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_89_arrow_Uparrowb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_90_arrow_Downarrowb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_91_arrow_Updownarrowb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_92_arrow_longleftrightarrowa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_93_arrow_Leftarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_94_arrow_Longleftarrowb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_95_arrow_Rightarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_96_arrow_Longrightarrowb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_97_arrow_Leftrightarrowb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_98_arrow_Longleftrightarrowb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_99_arrow_mapsto.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_100_arrow_longmapsto.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_101_arrow_nearrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_102_arrow_searrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_103_arrow_swarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_104_arrow_nwarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_105_arrow_hookleftarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_106_arrow_hookrightarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_107_arrow_rightleftharpoons.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_108_arrow_iff.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_109_arrow_leftharpoonup.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_110_arrow_rightharpoonup.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_111_arrow_leftharpoondown.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_112_arrow_rightharpoondown.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_113_other_because.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_114_other_therefore.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_115_other_dots.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_116_other_cdots.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_117_other_vdots.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_118_other_ddots.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_119_other_forall.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_120_other_exists.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_121_other_nexists.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_122_other_Finv.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_123_other_neg.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_124_other_prime.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_125_other_emptyset.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_126_other_infty.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_127_other_nabla.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_128_other_triangle.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_129_other_Box.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_130_other_Diamondb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_131_other_bot.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_132_other_top.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_133_other_angle.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_134_other_measuredangle.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_135_other_sphericalangle.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_136_other_surd.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_137_other_diamondsuit.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_138_other_heartsuit.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_139_other_clubsuit.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_140_other_spadesuit.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_141_other_flat.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_142_other_natural.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/symbol/symbol_143_other_sharp.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_1_lower_alpha.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_2_lower_beta.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_3_lower_gammaa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_4_lower_deltaa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_5_lower_epsilon.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_6_lower_varepsilon.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_7_lower_zeta.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_8_lower_eta.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_9_lower_thetaa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_10_lower_vartheta.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_11_lower_iota.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_12_lower_kappa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_13_lower_lambdaa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_14_lower_mu.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_15_lower_nu.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_16_lower_xia.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_17_lower_o.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_18_lower_pia.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_19_lower_varpi.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_20_lower_rho.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_21_lower_varrho.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_22_lower_sigmaa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_23_lower_varsigma.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_24_lower_tau.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_25_lower_upsilona.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_26_lower_phia.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_27_lower_varphi.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_28_lower_chi.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_29_lower_psia.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_30_lower_omegaa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_31_upper_Gammab.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_32_upper_Deltab.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_33_upper_Thetab.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_34_upper_Lambdab.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_35_upper_Xib.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_36_upper_Pib.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_37_upper_Sigmab.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_38_upper_Upsilonb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_39_upper_Phib.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_40_upper_Psib.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_41_upper_Omegab.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_42_other_hbar.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_43_other_imath.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_44_other_jmath.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_45_other_ell.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_46_other_Re.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_47_other_Im.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_48_other_aleph.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_49_other_beth.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_50_other_gimel.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_51_other_daleth.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_52_other_wp.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_53_other_mho.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_54_other_backepsilon.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_55_other_partial.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_56_other_eth.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_57_other_Bbbk.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_58_other_complement.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_59_other_circleds.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_60_other_S.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_61_other_mathbbABC.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_62_other_mathfrakABC.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_63_other_mathcalABC.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_64_other_mathrmABC.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/greek/greek_65_other_mathrmdef.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_1_frac_frac.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_2_frac_tfrac.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_3_frac_dif.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_4_frac_difa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_5_frac_partial.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_6_frac_partiala.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_7_frac_nabla.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_8_frac_partialb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_9_frac_cfrac.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_10_frac_cfraca.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_11_der_dot.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_12_der_ddot.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_13_der_prime.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_14_der_primea.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_15_der_primen.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_16_mod_bmod.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_17_mod_pmod.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_18_mod_gcd.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/frac/frac_19_mod_lcm.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_1_sqrt_sqrt.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_2_sqrt_sqrtn.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_3_superscript_topright.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_4_superscript_bottomright.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_5_superscript_right.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_6_superscript_left.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_7_superscript_sideset.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_8_other_hat.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_9_other_check.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_10_other_grave.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_11_other_acute.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_12_other_tilde.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_13_other_breve.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_14_other_bar.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_15_other_vec.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_16_other_not.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_17_other_degree.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_18_other_widetilde.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_19_other_widehat.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_20_other_overleftarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_21_other_overrightarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_22_other_overline_a.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_23_other_underline.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_24_other_overbrace.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_25_other_underbrace.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_26_other_overset.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_27_other_underset.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_28_other_stackrelfrown.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_29_other_overline_b.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_30_other_overleftrightarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_31_other_oversetleftarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_32_other_oversetrightarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_33_other_xleftarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sqrt/sqrt_34_other_xrightarrow.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_1_lim_lim.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_2_lim_limto0.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_3_lim_limtoinfty.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_4_lim_limtf.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_5_lim_max.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_6_lim_min.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_7_log_log.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_8_log_lg.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_9_log_ln.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_10_log_exp.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_11_bound_min.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_12_bound_max.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_13_bound_sup.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_14_bound_inf.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_15_bound_lim.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_16_bound_limsup.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_17_bound_liminf.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_18_bound_dim.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/limit/limit_19_bound_ker.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_1_sin.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_2_cos.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_3_tan.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_4_cot.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_5_sec.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_6_csc.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_7_insin.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_8_incos.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_9_intan.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_10_incot.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_11_insec.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_12_incsc.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_13_arcsin.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_14_arccos.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_15_arctan.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_16_arccot.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_17_arcsec.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_18_arccsc.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_19_sinh.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_20_cosh.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_21_tanh.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_22_coth.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_23_sech.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_24_csch.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_25_insinh.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_26_incosh.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_27_intanh.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_28_incoth.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_29_insech.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/trig/trig_30_incsch.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_1_int.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_2_inta.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_3_intb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_4_iint.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_5_iinta.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_6_iintb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_7_iiint.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_8_iiinta.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_9_iiintb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_10_oint.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/integral/integral_11_ointa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_1_sum_sum.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_2_sum_suma.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_3_sum_sumb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_4_prod_prod.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_5_prod_proda.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_6_prod_prodb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_7_prod_coprod.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_8_prod_coproda.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_9_prod_coprodb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_10_cup_cup.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_11_cup_cupa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_12_cup_cupb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_13_cup_cap.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_14_cup_capa.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_15_cup_capb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_16_vee_vee.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_17_vee_veea.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_18_vee_veeb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_19_vee_wedage.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_20_vee_wedagea.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/sum/sum_21_vee_wedageb.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_1_bracket_1.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_3_bracket_3.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_4_bracket_4.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_5_bracket_5.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_7_bracket_7.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_2_bracket_2.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_6_bracket_6.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_8_bracket_8.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_9_common_binom.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_10_common_interval.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_11_common_bra.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_12_common_ket.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/bracket/bracket_13_common_product.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/matrix/matrix_1_matrix.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/matrix/matrix_2_bmatrix.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/matrix/matrix_3_pmatrix.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/matrix/matrix_4_vmatrix.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/matrix/matrix_5_bigVmatrix.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/matrix/matrix_6_bigBmatrix.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/matrix/matrix_7_leftmatrix.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/matrix/matrix_8_rightmatrix.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/matrix/matrix_9_case.svg",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer2/matrix/matrix_10_align.svg"
]

PNG = [
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer1/symbol.png",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer1/greek.png",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer1/frac.png",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer1/sqrt.png",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer1/limit.png",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer1/trig.png",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer1/integral.png",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer1/sum.png",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer1/bracket.png",
"https://latexlive-resourse.oss-cn-beijing.aliyuncs.com/img/shortcut/layer1/matrix.png"
]
class Latex():
    # 初始化函数
    def __init__(self):
        self.baseUrl = 'https://www.latexlive.com/'
        self.name = 'svga'
        self.file_path = f'.//'+self.name+'//'
        #self.brower = webdriver.Chrome()
        if os.path.exists(self.file_path) == False:
            os.mkdir(self.file_path)
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                   'Accept':'*/*'
                   }

    def __del__(self):
        print(f'__del__')
        #self.file.close()
        #self.brower.close()

    #每个channel一个文件
    def open(self,channel):
        self.file = open(channel+".json", "a+",encoding='utf-8')

    #关闭文件
    def close(self):
        self.file.close()

    def getHtml(self,url):
        ''' 爬取网页数据 '''
        print(f"getHtml...{url}")
        self.headers['user-agent'] = random.choice(UA_LIST)
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'
        text = html.text
        print(text)
        return text


    #下载声音
    def download(self,link,filename):
        try:
            self.headers['user-agent'] = random.choice(UA_LIST)
            pic = requests.get(link,headers=self.headers)
            print(pic.status_code)
            if pic.status_code == 200:
                with open(os.path.join(self.file_path) + os.sep + filename, 'wb') as fp:
                    print("file:",os.path.join(self.file_path) + os.sep + filename)
                    fp.write(pic.content)
                    fp.close()
            print("下载完成")
        except Exception as e:
            print(e)

    #获取声音url
    def getSound(self,url,name):
        print(f"sound url:{url}")
        #html = self.getHtml(url)

        self.brower.get(url)
        #print(self.brower.page_source)
        #more = brower.find_element_by_xpath('//div[@class="unfold-field_text"]/span')
        #more.click()
        wait = WebDriverWait(self.brower, 20)
        #element = wait.until(EC.presence_of_element_located((By.ID, 'jquery_jplayer_1')))
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="jquery_jplayer_1"]/audio')))
        #element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="jquery_jplayer_1"]/audio')))
        print(element)
        # 设定页面加载限制时间
        #self.brower.set_page_load_timeout(25)
        #return self.parseSoundUrl(html)

        player = self.brower.find_element_by_xpath('//div[@id="jquery_jplayer_1"]/audio')

        # print(jplayer)
        # print(player.find_element_by_xpath('./audio/@src'))
        print(player.get_attribute('src'))

        value = {}
        value['audio'] = player.get_attribute('src')
        audioname = os.path.basename(value['audio'])
        kname = str(name)
        audioname = self.name+"_"+kname.zfill(3)+".mp3"
        self.download(value['audio'], audioname)
        return value['audio']

    def getUrl(self,url):
        print(f"sound url:{url}")
        #html = self.getHtml(url)

        self.brower.get(url)
        print(self.brower.page_source)
        #more = brower.find_element_by_xpath('//div[@class="unfold-field_text"]/span')
        #more.click()
        wait = WebDriverWait(self.brower, 20)
        value = {}
        return value['audio']

    def parseSound(self):
        self.open(self.name)
        for value in range(1,181):
            huibenurl = self.baseUrl.format(value)
            if value == 1:
                huibenurl = self.baseUrl1
            #huibenHtml = self.getHtml(huibenurl)
            values = {}
            values['audio'] = self.getSound(huibenurl,value)
            kname = str(value)
            values['name'] = kname.zfill(3)
            self.file.write(str(values).encode('utf-8').decode('utf-8'))
            self.file.write(f'\n')
            #self.parseHtml(huibenHtml)
        self.close()
    def downloadsvg(self):
        for i in range(0,len(PNG)):
            url = PNG[i]
            name = os.path.basename(url)
            print("url:",url,"name:",name)
            self.download(url,name)
    def parseLatex(self):
        html = self.getUrl(self.baseUrl)
if __name__ == '__main__':
    latex = Latex()
    latex.downloadsvg()
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
import time

driver = webdriver.Chrome()
driver.get('https://www.youshenghuiben.com/guoneihuiben/woyaobanchuqu127.html')

# print(driver.page_source)
more = driver.find_element_by_xpath('//div[@class="unfold-field_text"]/span')
more.click()
containets = driver.find_elements_by_xpath('//div[@id="containet"]/ul[@id="pageMain"]/li')

# 设定页面加载限制时间
driver.set_page_load_timeout(10)

# print(containets.size)
for containet in containets:
    print(containet.text)

wait = WebDriverWait(driver, 30)
# element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="btn btn-search"]')))

jplayers = driver.find_element_by_xpath(
    '//div[@id="jp_container_1"]/div[@class="jp-type-single"]/div[@class="jp-gui jp-interface"]/div[@class="jp-controls"]/button')
# jplayer.click()
# js = driver.execute_script("arguments[0].click();", jplayers)
# print(driver.execute_script('return document.getElementById("jquery_jplayer_1").innerText'))

# driver.executeScript("arguments[0].click();",jplayers);

print(driver.page_source)

player = driver.find_element_by_xpath('//div[@id="jquery_jplayer_1"]')

# print(jplayer)
print(player.find_element_by_xpath('./audio/@src'))

'''