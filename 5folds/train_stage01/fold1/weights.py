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
            class_weights.append({1:0.7232649879724663,0:0.2767350120275337})
        if(str(class_name) == 'Pneumonia' or str(class_name) == 'pneumonia'): #2
            class_weights.append({0:0.8907362103995036,1:0.10926378960049644})
        if(str(class_name) == 'Fibrosis' or str(class_name) == 'fibrosis'): #3
            class_weights.append({0:0.8919768711724897,1:0.10802312882751028})
        if(str(class_name) == 'Edema' or str(class_name) == 'edema'): #4
            class_weights.append({0:0.9319134537175323,1:0.06808654628246767})
        if(str(class_name) == 'Emphysema' or str(class_name) == 'emphysema'): #5
            class_weights.append({0:0.9337746340305197,1:0.0662253659694802})
        if(str(class_name) == 'Cardiomegaly' or str(class_name) == 'cardiomegaly'): #6
            class_weights.append({0:0.9346911422011416,1:0.06530885779885844})
        if(str(class_name) == 'Pleural_Thickening' or str(class_name) == 'pleural_thickening' or str(class_name) == 'Pleural_thickening' or str(class_name) == 'pleural_Thickening'): #7
            class_weights.append({0:0.9471485596559489,1:0.05285144034405107})
        if(str(class_name) == 'Pneumothorax' or str(class_name) == 'pneumothorax'): #8
            class_weights.append({0:0.9597849732593348,1:0.04021502674066528})
        if(str(class_name) == 'Consolidation' or str(class_name) == 'consolidation'): #9
            class_weights.append({0:0.9634215851547732,1:0.03657841484522683})
        if(str(class_name) == 'Mass' or str(class_name) == 'mass'): #10
            class_weights.append({0:0.9664815596284937,1:0.033518440371506274})
        if(str(class_name) == 'Nodule' or str(class_name) == 'nodule'): #11
            class_weights.append({0:0.9675226255494984,1:0.03247737445050164})
        if(str(class_name) == 'Atelectasis' or str(class_name) == 'atelectasis'): #12
            class_weights.append({0:0.9767642443073444,1:0.023235755692655607})
        if(str(class_name) == 'Effusion' or str(class_name) == 'effusion'): #13
            class_weights.append({0:0.9783086050790473,1:0.021691394920952775})
        if(str(class_name) == 'Infiltration' or str(class_name) == 'infiltration'): #4
            class_weights.append({0:0.9807405238168388,1:0.019259476183161137})
    return class_weights
