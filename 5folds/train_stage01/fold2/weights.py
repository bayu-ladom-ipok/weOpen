import numpy as np


def get_class_weights(total_counts, class_positive_counts, multiply):
    """
    Calculate class_weight used in training

    Arguments:
    total_counts - int
    class_positive_counts - dict of int, ex: {"Effusion": 300, "Infiltration": 500 ...}
    multiply - int, positve weighting multiply
    use_class_balancing - boolean 

    Returns:
    class_weight - dict of dict, ex: {"Effusion": { 0: 0.01, 1: 0.99 }, ... }
    """
    def get_single_class_weight(pos_counts, total_counts):
        denominator = (total_counts - pos_counts) * multiply + pos_counts
        return {
            0: pos_counts / denominator,
            1: (denominator - pos_counts) / denominator,
        }

    class_names = list(class_positive_counts.keys())
    label_counts = np.array(list(class_positive_counts.values()))
    class_weights = []
    for i, class_name in enumerate(class_names):
        if(str(class_name) == 'Hernia' or str(class_name) == 'hernia'): #1
            class_weights.append({1:0.7256727746991359,0:0.27432722530086406})
        if(str(class_name) == 'Pneumonia' or str(class_name) == 'pneumonia'): #2
            class_weights.append({0:0.887935276542454,1:0.11206472345754603})
        if(str(class_name) == 'Fibrosis' or str(class_name) == 'fibrosis'): #3
            class_weights.append({0:0.9031195338385782,1:0.09688046616142172})
        if(str(class_name) == 'Edema' or str(class_name) == 'edema'): #4
            class_weights.append({0:0.9258206073343399,1:0.07417939266566007})
        if(str(class_name) == 'Emphysema' or str(class_name) == 'emphysema'): #5
            class_weights.append({0:0.9309613322488964,1:0.06903866775110355})
        if(str(class_name) == 'Cardiomegaly' or str(class_name) == 'cardiomegaly'): #6
            class_weights.append({0:0.9400356590754857,1:0.05996434092451428})
        if(str(class_name) == 'Pleural_Thickening' or str(class_name) == 'pleural_thickening' or str(class_name) == 'Pleural_thickening' or str(class_name) == 'pleural_Thickening'): #7
            class_weights.append({0:0.9486159014030188,1:0.051384098596981266})
        if(str(class_name) == 'Pneumothorax' or str(class_name) == 'pneumothorax'): #8
            class_weights.append({0:0.9593917661953634,1:0.04060823380463664})
        if(str(class_name) == 'Consolidation' or str(class_name) == 'consolidation'): #9
            class_weights.append({0:0.9624335988009675,1:0.03756640119903254})
        if(str(class_name) == 'Mass' or str(class_name) == 'mass'): #10
            class_weights.append({0:0.9650087881222735,1:0.034991211877726434})
        if(str(class_name) == 'Nodule' or str(class_name) == 'nodule'): #11
            class_weights.append({0:0.9673527498604587,1:0.032647250139541326})
        if(str(class_name) == 'Atelectasis' or str(class_name) == 'atelectasis'): #12
            class_weights.append({0:0.9763749017961535,1:0.023625098203846454})
        if(str(class_name) == 'Effusion' or str(class_name) == 'effusion'): #13
            class_weights.append({0:0.9779771730916857,1:0.022022826908314256})
        if(str(class_name) == 'Infiltration' or str(class_name) == 'infiltration'): #4
            class_weights.append({0:0.9806454863894606,1:0.019354513610539362})
    return class_weights
