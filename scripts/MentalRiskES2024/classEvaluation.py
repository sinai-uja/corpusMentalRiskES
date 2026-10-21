#This file has been developed by the SINAI research group for its usage in the MentalRiskES evaluation campaign at IberLEF 2024

# Required libraries
import pandas as pd
import numpy as np
import sklearn.metrics as metrics
import statistics
from typing import Dict

def read_gold_multiclass(gold_file: str):
    """ Read gold labels for multiclass classification (task1) and save it into a dict
        Args:
            gold_file (str): path to the location of the file with the labels: gold.txt
        Returns:
            gold_b (Dict): dict of subject with their gold labels as int
            gold_label (Dict): dict of subject with their gold labels as str    
    """
    gold_label = {}
    gold_b = {}
    df_golden_truth = pd.read_csv(gold_file)
    for index, r in df_golden_truth.iterrows():
        gold_label[ r['Subject'] ] = r['label']
        gold_b[ r['Subject'] ] = 0 if r['label'] == 'none' else 1
    print("\n"+str(len(gold_b))+ " lines read in gold file!\n\n")
    return gold_b, gold_label

def read_gold_contexts(gold_file: str):
    """ Read gold labels for multiclass classification with two levels (task2) and save it into a dict
        Args:
            gold_file (str): path to the location of the file with the labels: gold.txt
        Returns:
            gold_b (Dict): dict of subject with their gold labels as int
            gold_label (Dict): dict of subject with their gold labels as str
            gold_contexts (Dict): dict of dicts of contexts with subject with their gold labels        
    """
    gold_label = {}
    gold_b = {}
    gold_contexts = {}
    contexts = ['addiction','emergency','family','work','social','other','none'] # order is important
        
    df_golden_truth = pd.read_csv(gold_file)
    for index, r in df_golden_truth.iterrows():
        gold_label[ r['Subject'] ] = r['label']
        gold_b[ r['Subject'] ] = 0 if r['label'] == 'none' else 1
        gold_contexts[r['Subject']] = []
        for c in contexts:
            gold_contexts[r['Subject']].append(r[c])

    print("\n"+str(len(gold_b))+ " lines read in gold file!\n\n")
    return gold_b, gold_label, gold_contexts

def read_gold_binary(gold_file: str):
    """ Read gold labels for binary classification (task3) and save it into a dict
        Args:
            gold_file (str): path to the location of the file with the labels: gold.txt
        Returns:
            gold_b (Dict): dict of subject with their gold labels as int
            gold_label (Dict): dict of subject with their gold labels as str    
    """
    gold_label = {}
    gold_b = {}
    df_golden_truth = pd.read_csv(gold_file)
    for index, r in df_golden_truth.iterrows():
        gold_b[ r['Subject'] ] = r['label']
    print("\n"+str(len(gold_b))+ " lines read in gold file!\n\n")
    return gold_b, gold_label


class multiclassClassification():
    """ Calculation of metrics for multiclass classification tasks
        Attributes:
            json_path (str): path to the file with the sent final prediction. This file has the following structure: 
                {
                "subject1": {
                    "pred_b": 0,
                    "pred": "none",
                    "round": 50 # last round because this subject did not predict as positive
                    },
                "subject2": {
                    "pred_b": 1,
                    "pred": "anxiety",
                    "round": 8 # althought this subject would have been predicted as negative after round 8, it does not change anything
                    },
                    ...
                }
            gold (Dict): dict with gold labels
    """
    def __init__(self, json_path: str, gold: Dict):
        run_results = pd.read_json(json_path).T
        run_results['nick'] = run_results.index
        run_results = run_results.reset_index(drop=True)
        self.run_results = run_results.sort_values(by=['nick'])
        self.gold_b, self.gold_label = read_gold_multiclass(gold)
    pass

    def penalty(self, delay):
        p = 0.0314 # = -(LN(0,33)/(AVG_NUM_POSTS_PER_USER-1))
        pen = -1.0 + 2.0/(1+np.exp(-p*(delay-1)))
        return(pen)

    def n_pos(self):
        total_pos = 0
        for key in self.gold_b:
            total_pos += self.gold_b[key]
        return(total_pos)

    def eval_performance(self):
        print("===================================================")
        print("EVALUATION:") 
        total_pos=self.n_pos()
        erdes5 = np.zeros(len(self.run_results))
        erdes30 = np.zeros(len(self.run_results))
        ierdes = 0
        true_pos = 0
        false_pos = 0
        latency_tps = list()
        penalty_tps = list()

        for index, r in self.run_results.iterrows():
            try:
                if ( self.gold_b[ r['nick'] ] ==  r['pred_b'] ):
                    if ( r['pred_b'] == 1 ): # True positive
                        true_pos+=1
                        erdes5[ierdes] = 1.0 - (1.0/(1.0+np.exp( (r["round"]+1) - 5.0)))
                        erdes30[ierdes] = 1.0 - (1.0/(1.0+np.exp( (r["round"]+1) - 30.0)))
                        latency_tps.append(r["round"]+1)
                        penalty_tps.append(self.penalty(r["round"]+1))
                    else: # True negative
                        erdes5[ierdes] = 0
                        erdes30[ierdes] = 0
                else:
                    if ( r['pred_b'] == 1 ): # False positive
                        false_pos+=1
                        erdes5[ierdes] = float(total_pos) / float(len(self.gold_b))
                        erdes30[ierdes] = float(total_pos) / float(len(self.gold_b))
                    else: # False negative
                        erdes5[ierdes] = 1
                        erdes30[ierdes] = 1
            except KeyError:
                print("User does not appear in the gold:"+r['nick'])
            ierdes+=1

        _speed = 1-np.median(np.array(penalty_tps))
        if true_pos != 0 :
            precision = float(true_pos) / float(true_pos+false_pos)    
            recall = float(true_pos) / float(total_pos)
            f1_erde = 2 * (precision * recall) / (precision + recall)
            _latencyweightedF1 = f1_erde*_speed
        else:
            _latencyweightedF1 = 0
            _speed = 0
            
        y_pred_b = self.run_results['pred'].tolist()
        y_true  = list(self.gold_label.values())

        # Metrics
        accuracy = metrics.accuracy_score(y_true, y_pred_b)
        macro_precision = metrics.precision_score(y_true, y_pred_b, average='macro')
        macro_recall = metrics.recall_score(y_true, y_pred_b, average='macro')
        macro_f1 = metrics.f1_score(y_true, y_pred_b, average='macro')
        micro_precision = metrics.precision_score(y_true, y_pred_b, average='micro')
        micro_recall = metrics.recall_score(y_true, y_pred_b, average='micro')
        micro_f1 = metrics.f1_score(y_true, y_pred_b, average='micro')

        print("BINARY METRICS: =============================")
        print("Accuracy:"+str(accuracy))
        print("Macro precision:"+str(macro_precision))
        print("Macro recall:"+str(macro_recall))
        print("Macro f1:"+str(macro_f1))
        print("Micro precision:"+str(micro_precision))
        print("Micro recall:"+str(micro_recall))
        print("Micro f1:"+str(micro_f1))

        print("LATENCY-BASED METRICS: =============================")
        print("ERDE_5:"+str(np.mean(erdes5)))
        print("ERDE_30:"+str(np.mean(erdes30)))
        print("Median latency:"+str(np.median(np.array(latency_tps)))) 
        print("Speed:"+str(_speed)) 
        print("latency-weightedF1:"+str(_latencyweightedF1)) 
        
        return {'Acuracy': accuracy, 'Macro_P': macro_precision, 'Macro_R': macro_recall,'Macro_F1': macro_f1,'Micro_P': micro_precision, 'Micro_R': micro_recall,
        'Micro_F1': micro_f1, 'ERDE5':np.mean(erdes5),'ERDE30': np.mean(erdes30), 'latencyTP': np.median(np.array(latency_tps)), 
        'speed': _speed, 'latency-weightedF1': _latencyweightedF1}
    

class twolevelMulticlassClassification():
    """ Calculation of metrics for two level multiclass classification task
        Attributes:
            json_path (str): path to the file with the sent final prediction. This file has the following structure: 
                {
                "subject1": {
                    "pred_b": 0,
                    "pred": "none",
                    "contexts": "none" # must be none because the pred is none
                    "contexts_b": [0, 0, 0, 0, 0, 0, 0], #'addiction','emergency','family','work','social','other','none'
                    "round": 50 # last round because this subject did not predict as positive
                    },
                "subject2": {
                    "pred_b": 1,
                    "pred": "anxiety",
                    "contexts": "family#work#social", # contexts concatenated with '#' symbol
                    "contexts_b": [0, 0, 1, 1, 1, 0, 0], #'addiction','emergency','family','work','social','other','none'
                    "round": 8, # althought this subject would have been predicted as negative after round 8, it does not change anything
                    },
                    ...
                }
            gold (Dict): dict with gold labels
    """
    def __init__(self, json_path: str, gold: Dict):
        run_results = pd.read_json(json_path).T
        run_results['nick'] = run_results.index
        run_results = run_results.reset_index(drop=True)
        self.run_results = run_results.sort_values(by=['nick'])
        self.gold_b, self.gold_label, self.gold_contexts = read_gold_contexts(gold)
    pass

    def penalty(self, delay):
        p = 0.0314
        pen = -1.0 + 2.0/(1+np.exp(-p*(delay-1)))
        return(pen)

    def n_pos(self):
        total_pos = 0
        for key in self.gold_b:
            total_pos += self.gold_b[key]
        return(total_pos)

    def eval_performance(self):
        print("===================================================")
        print("EVALUATION:") 
        total_pos=self.n_pos()
        erdes5 = np.zeros(len(self.run_results))
        erdes30 = np.zeros(len(self.run_results))
        ierdes = 0
        true_pos = 0
        false_pos = 0
        latency_tps = list()
        penalty_tps = list()

        for index, r in self.run_results.iterrows():
            try:
                if ( self.gold_b[ r['nick'] ] ==  r['pred_b'] ):
                    if ( r['pred_b'] == 1 ):  # True positive
                        true_pos+=1
                        erdes5[ierdes] = 1.0 - (1.0/(1.0+np.exp( (r["round"]+1) - 5.0)))
                        erdes30[ierdes] = 1.0 - (1.0/(1.0+np.exp( (r["round"]+1) - 30.0)))
                        latency_tps.append(r["round"]+1)
                        penalty_tps.append(self.penalty(r["round"]+1))
                    else:  # True negative
                        erdes5[ierdes] = 0
                        erdes30[ierdes] = 0
                else:
                    if ( r['pred_b'] == 1 ): # False positive
                        false_pos+=1
                        erdes5[ierdes] = float(total_pos) / float(len(self.gold_b))
                        erdes30[ierdes] = float(total_pos) / float(len(self.gold_b))
                    else: # False negative
                        erdes5[ierdes] = 1
                        erdes30[ierdes] = 1
            except KeyError:
                print("User does not appear in the gold:"+r['nick'])
            ierdes+=1

        _speed = 1-np.median(np.array(penalty_tps))
        if true_pos != 0 :
            precision = float(true_pos) / float(true_pos+false_pos)    
            recall = float(true_pos) / float(total_pos)
            f1_erde = 2 * (precision * recall) / (precision + recall)
            _latencyweightedF1 = f1_erde*_speed
        else:
            _latencyweightedF1 = 0
            _speed = 0
            
        y_pred_b = self.run_results['pred'].tolist()
        y_true  = list(self.gold_label.values())

        y_contexts_b = self.run_results['contexts_b'].tolist()
        y_contexts_true  = list(self.gold_contexts.values())
        
        # Metrics for predictions
        accuracy = metrics.accuracy_score(y_true, y_pred_b)
        macro_precision = metrics.precision_score(y_true, y_pred_b, average='macro')
        macro_recall = metrics.recall_score(y_true, y_pred_b, average='macro')
        macro_f1 = metrics.f1_score(y_true, y_pred_b, average='macro')
        micro_precision = metrics.precision_score(y_true, y_pred_b, average='micro')
        micro_recall = metrics.recall_score(y_true, y_pred_b, average='micro')
        micro_f1 = metrics.f1_score(y_true, y_pred_b, average='micro')

        # Metrics for contexts
        accuracy_c = metrics.accuracy_score(y_contexts_true, y_contexts_b)
        macro_precision_c = metrics.precision_score(y_contexts_true, y_contexts_b, average='macro')
        macro_recall_c = metrics.recall_score(y_contexts_true, y_contexts_b, average='macro')
        macro_f1_c = metrics.f1_score(y_contexts_true, y_contexts_b, average='macro')
        micro_precision_c = metrics.precision_score(y_contexts_true, y_contexts_b, average='micro')
        micro_recall_c = metrics.recall_score(y_contexts_true, y_contexts_b, average='micro')
        micro_f1_c = metrics.f1_score(y_contexts_true, y_contexts_b, average='micro')

        print("BINARY METRICS: =============================")
        print("Accuracy:"+str(accuracy))
        print("Macro precision:"+str(macro_precision))
        print("Macro recall:"+str(macro_recall))
        print("Macro f1:"+str(macro_f1))
        print("Micro precision:"+str(micro_precision))
        print("Micro recall:"+str(micro_recall))
        print("Micro f1:"+str(micro_f1))

        print("LATENCY-BASED METRICS: =============================")
        print("ERDE_5:"+str(np.mean(erdes5)))
        print("ERDE_30:"+str(np.mean(erdes30)))
        print("Median latency:"+str(np.median(np.array(latency_tps)))) 
        print("Speed:"+str(_speed)) 
        print("latency-weightedF1:"+str(_latencyweightedF1))

        print("BINARY METRICS CONTEXTS: =============================")
        print("Accuracy:"+str(accuracy_c))
        print("Macro precision:"+str(macro_precision_c))
        print("Macro recall:"+str(macro_recall_c))
        print("Macro f1:"+str(macro_f1_c))
        print("Micro precision:"+str(micro_precision_c))
        print("Micro recall:"+str(micro_recall_c))
        print("Micro f1:"+str(micro_f1_c))
        
        return {'Acuracy': accuracy, 'Macro_P': macro_precision, 'Macro_R': macro_recall,'Macro_F1': macro_f1,'Micro_P': micro_precision, 'Micro_R': micro_recall,
        'Micro_F1': micro_f1, 'ERDE5':np.mean(erdes5),'ERDE30': np.mean(erdes30), 'latencyTP': np.median(np.array(latency_tps)), 
        'speed': _speed, 'latency-weightedF1': _latencyweightedF1,'Acuracy_c': accuracy_c, 'Macro_P_c': macro_precision_c, 'Macro_R_c': macro_recall_c,
        'Macro_F1_c': macro_f1_c,'Micro_P_c': micro_precision_c, 'Micro_R_c': micro_recall_c,'Micro_F1_c': micro_f1_c}

###########################################################################
class  binaryClassification():
    """ Calculation of metrics for binary classification tasks
        Attributes:
            json_path (str): path to the file with the sent final prediction. This file has the following structure: 
                {
                "subject1": {
                    "pred_b": 0,
                    "round": 50 # last round because this subject did not predict as positive
                    },
                "subject2": {
                    "pred_b": 1,
                    "round": 8 # althought this subject would have been predicted as negative after round 8, it does not change anything
                    },
                    ...
                }
            gold (Dict): dict with gold labels
    """
    def __init__(self, json_path: str, gold: Dict):
        run_results = pd.read_json(json_path).T
        run_results['nick'] = run_results.index
        run_results = run_results.reset_index(drop=True)
        self.run_results = run_results.sort_values(by=['nick'])
        self.gold_b, self.gold_label = read_gold_binary(gold)
    pass

    def penalty(self, delay):
        p = 0.0199
        pen = -1.0 + 2.0/(1+np.exp(-p*(delay-1)))
        return(pen)

    def n_pos(self):
        total_pos = 0
        for key in self.gold_b:
            total_pos += self.gold_b[key]
        return(total_pos)

    def eval_performance(self):
        print("===================================================")
        print("EVALUATION:") 
        total_pos=self.n_pos()
        erdes5 = np.zeros(len(self.run_results))
        erdes30 = np.zeros(len(self.run_results))
        ierdes = 0
        true_pos = 0
        false_pos = 0
        latency_tps = list()
        penalty_tps = list()

        for index, r in self.run_results.iterrows():
            try:
                if ( self.gold_b[ r['nick'] ] ==  r['pred_b'] ):
                    if ( r['pred_b'] == 1 ): # True positive
                        true_pos+=1
                        erdes5[ierdes] = 1.0 - (1.0/(1.0+np.exp( (r["round"]+1) - 5.0)))
                        erdes30[ierdes] = 1.0 - (1.0/(1.0+np.exp( (r["round"]+1) - 30.0)))
                        latency_tps.append(r["round"]+1)
                        penalty_tps.append(self.penalty(r["round"]+1))
                    else: # True negative
                        erdes5[ierdes] = 0
                        erdes30[ierdes] = 0
                else:
                    if ( r['pred_b'] == 1 ): # False positive
                        false_pos+=1
                        erdes5[ierdes] = float(total_pos) / float(len(self.gold_b))
                        erdes30[ierdes] = float(total_pos) / float(len(self.gold_b))
                    else: # False negative
                        erdes5[ierdes] = 1
                        erdes30[ierdes] = 1
            except KeyError:
                print("User does not appear in the gold:"+r['nick'])
            ierdes+=1

        _speed = 1-np.median(np.array(penalty_tps))
        if true_pos != 0 :
            precision = float(true_pos) / float(true_pos+false_pos)    
            recall = float(true_pos) / float(total_pos)
            f1_erde = 2 * (precision * recall) / (precision + recall)
            _latencyweightedF1 = f1_erde*_speed
        else:
            _latencyweightedF1 = 0
            _speed = 0
            
        y_pred_b = self.run_results['pred'].tolist()
        y_true  = list(self.gold_label.values())

        # Metrics
        accuracy = metrics.accuracy_score(y_true, y_pred_b)
        macro_precision = metrics.precision_score(y_true, y_pred_b, average='macro')
        macro_recall = metrics.recall_score(y_true, y_pred_b, average='macro')
        macro_f1 = metrics.f1_score(y_true, y_pred_b, average='macro')
        micro_precision = metrics.precision_score(y_true, y_pred_b, average='micro')
        micro_recall = metrics.recall_score(y_true, y_pred_b, average='micro')
        micro_f1 = metrics.f1_score(y_true, y_pred_b, average='micro')

        print("BINARY METRICS: =============================")
        print("Accuracy:"+str(accuracy))
        print("Macro precision:"+str(macro_precision))
        print("Macro recall:"+str(macro_recall))
        print("Macro f1:"+str(macro_f1))
        print("Micro precision:"+str(micro_precision))
        print("Micro recall:"+str(micro_recall))
        print("Micro f1:"+str(micro_f1))

        print("LATENCY-BASED METRICS: =============================")
        print("ERDE_5:"+str(np.mean(erdes5)))
        print("ERDE_30:"+str(np.mean(erdes30)))
        print("Median latency:"+str(np.median(np.array(latency_tps)))) 
        print("Speed:"+str(_speed)) 
        print("latency-weightedF1:"+str(_latencyweightedF1)) 
        
        return {'Acuracy': accuracy, 'Macro_P': macro_precision, 'Macro_R': macro_recall,'Macro_F1': macro_f1,'Micro_P': micro_precision, 'Micro_R': micro_recall,
        'Micro_F1': micro_f1, 'ERDE5':np.mean(erdes5),'ERDE30': np.mean(erdes30), 'latencyTP': np.median(np.array(latency_tps)), 
        'speed': _speed, 'latency-weightedF1': _latencyweightedF1}

class Emissions():
    """ Class for calculating carbon emission values
        Attributes:
            emissions_run (Dict[List]): dict whose keys are the emissions values requested and the values are lists with the items obtained for each round
    """
    def __init__(self, emissions_run) -> None:
        self.emissions_run = emissions_run
        self.aux = {}
        for key, value in emissions_run.items():
            self.aux[key] = 0
        pass

    # Update of values after a prediction has been made
    def update_emissions(self, emissions_round):
        # The values are accumulated in each round, so the difference is calculated to know the values for that round only
        if len(emissions_round.items()) != 0:
            if emissions_round['duration'] - self.aux['duration'] < 0 :
                print("RESETEO: ", self.emissions_run)
                for key, value in self.aux.items():
                    self.aux[key] = 0
            for key, value in self.emissions_run.items():
                if key not in ["cpu_count","gpu_count","cpu_model","gpu_model", "ram_total_size","country_iso_code"]:
                    round_ = emissions_round[key] - self.aux[key]
                    self.emissions_run[key].append(round_)
                    self.aux[key] = emissions_round[key]
                else:
                    self.emissions_run[key] = emissions_round[key]
        else:
            print("Empty: ", self.emissions_run)
            for key, value in self.aux.items():
                self.aux[key] = 0

    # Calculation of final values after all predictions have been made
    def calculate_emissions(self):
        dict_ = {}
        for key, value in self.emissions_run.items():
            # Non-numerical values
            if key in ["cpu_count","gpu_count","cpu_model","gpu_model", "ram_total_size","country_iso_code"]:
                dict_[key] = self.emissions_run[key]
            else: # Numerical values
                dict_[key+"_min"] = min(self.emissions_run[key])
                dict_[key+"_max"] = max(self.emissions_run[key])
                dict_[key+"_mean"] = sum(self.emissions_run[key])/len(self.emissions_run[key])
                dict_[key+"_desv"] = statistics.pstdev(self.emissions_run[key])
        return dict_