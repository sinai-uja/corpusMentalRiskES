#This file has been developed by the SINAI research group for its usage in the MentalRiskES evaluation campaign at IberLEF 2023

# Required libraries
import pandas as pd
import numpy as np
import sklearn.metrics as metrics
from scipy.stats import pearsonr
import os
import statistics
from typing import Dict

def read_gold(gold_file: str):
    """ Read gold labels for binary classification (task1a, task2a, and task3a) and save it into a dict
        Args:
            gold_file (str): path to the location of the file with the labels: gold.txt
        Returns:
            gold (Dict): dict of subject with their gold labels as int 
    """
    gold_b = {}
    df_golden_truth = pd.read_csv(gold_file)
    for index, r in df_golden_truth.iterrows():
        gold_b[ r['Subject'] ] = int(r['label'])
    print("\n"+str(len(gold_b))+ " lines read in gold file!\n\n")
    return gold_b

def read_gold_regression(gold_file: str):
    """ Read gold labels for simple regression (task1b, task2b and task3b) and save it into a dict
        Args:
            gold_file (str): path to the location of the file with the labels: gold.txt
        Returns:
            gold (Dict): dict of subject with their gold labels as float 
    """
    gold = {}
    df_golden_truth = pd.read_csv(gold_file)
    for index, r in df_golden_truth.iterrows():
        gold[ r['Subject'] ] = float(r['label'])
    print("\n"+str(len(gold))+ " lines read in gold file!\n\n")
    return gold

def read_gold_multiclass(gold_file: str):
    """ Read gold labels for multiclass classification (task2c) and save it into a dict
        Args:
            gold_file (str): path to the location of the file with the labels: gold.txt
        Returns:
            gold_b (Dict): dict of subject with their gold labels as int
            gold_label (Dict): dict of subject with their gold labels as str    
    """
    gold_b = {}
    gold_label = {}
    df_golden_truth = pd.read_csv(gold_file)
    for index, r in df_golden_truth.iterrows():
        gold_label[ r['Subject'] ] = r['label']
        gold_b[ r['Subject'] ] = 1 if "suffer" in r['label'] else 0
    print("\n"+str(len(gold_b))+ " lines read in gold file!\n\n")
    return gold_b, gold_label

def read_gold_multioutput(gold_file):
    """ Read gold labels formulti-output regression (task2d) and save it into a dict
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
        gold_label[ r['Subject'] ] = [r['suffer_in_favour'],r['suffer_against'],r['suffer_other'],r['control']]
    print("\n"+str(len(gold_label))+ " lines read in gold file!\n\n")

    for subject, values in gold_label.items():
        max_index = values.index(max(values))
        gold_b[subject] = [1 if i == max_index else 0 for i in range(len(values))]
    return gold_label, gold_b

###########################################################################
class BinaryClassification():
    """ Calculation of Binary classification metrics for Binary classification tasks
        Attributes:
            task (str): task to be adressed
            data (DataFrame): table with the sent final prediction. This file has the following structure: 
            gold (Dict): dict with gold labels
    """
    def __init__(self, task: str, data, gold: Dict):
        self.run_results = data 
        self.gold_b = read_gold(gold)
        self.task = task
    pass

    def penalty(self,delay):
        if self.task == "1": # TCA
            p = 0.0292 # trial
            p = 0.0411 # test
        elif self.task == "2": # Depression
            p = 0.0179 # trial
            p = 0.0326 # test
        else: # Unkown
            p = 0.0308 # test
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
        self.run_results = self.run_results.sort_values(by=['nick'])
        total_pos=self.n_pos()
        erdes5 = np.zeros(len(self.run_results))
        erdes30 = np.zeros(len(self.run_results))
        ierdes = 0
        true_pos = 0
        false_pos = 0
        latency_tps = list()
        penalty_tps = list()

        # Latency-based metrics
        for index, r in self.run_results.iterrows():
            try:
                if ( self.gold_b[ r['nick'] ] ==  r['pred'] ):
                    if ( r['pred'] == 1 ): # True positive
                        true_pos+=1
                        erdes5[ierdes]=1.0 - (1.0/(1.0+np.exp( (r["round"]+1) - 5.0)))
                        erdes30[ierdes]=1.0 - (1.0/(1.0+np.exp( (r["round"]+1) - 30.0)))
                        latency_tps.append(r["round"]+1)
                        penalty_tps.append(self.penalty(r["round"]+1))
                    else: # True negative
                        erdes5[ierdes]=0
                        erdes30[ierdes]=0
                else:
                    if ( r['pred'] == 1 ): # False positive
                        false_pos+=1
                        erdes5[ierdes]=float(total_pos)/float(len(self.gold_b))
                        erdes30[ierdes]=float(total_pos)/float(len(self.gold_b))
                    else: # False negative
                        erdes5[ierdes]=1
                        erdes30[ierdes]=1
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
        y_true = list(self.gold_b.values()) 

        # Binary metrics
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


#############################################################################################
class ClassRegressionEvaluation():
    """ Calculation of regression metrics for simple regression tasks
        Attributes:
            task (str): task to be adressed
            data (DataFrame): table with the sent final prediction. This file has the following structure: 
            gold (Dict): dict with gold labels
    """
    def __init__(self, task: str, data, gold: Dict):
        self.run_results = data 
        self.gold = read_gold_regression(gold)
        self.gold_b = read_gold(gold)
        self.task = task

    def eval_performance(self):
        self.run_results = self.run_results.sort_values(by=['nick'])
        y_pred_r = self.run_results['pred'].tolist() 
        y_true = list(self.gold.values()) 

        # Regression metrics
        _rmse = metrics.mean_squared_error(y_true, y_pred_r, squared=False)
        _pearson, _ = pearsonr(y_true, y_pred_r)

        print("REGRESSION METRICS: =============================")
        print("RMSE:"+str(_rmse))
        print("Pearson correlation coefficient:"+str(_pearson))
        return { 'RMSE': _rmse, 'Pearson_coefficient': _pearson}
    
    # Calculation of P@5, P@10, P@20, P@30
    def eval_performance_rank_based(self,results_rank1,results_rank2,results_rank3,results_rank4):
        print("===================================================")
        print("RANK-BASED EVALUATION:")
        results_at=[results_rank1,results_rank2,results_rank3,results_rank4]
        rank_dit = {}
        for results in results_at:
            rank = results.split("_")[-1].split(".")[0]
            print("Analizing ranking at round "+rank)
            p = []
            if os.path.exists(results):
                run_results = pd.read_json(results,orient='index').sort_values(by=['pred'],ascending=False) 
                print(run_results)
                run_results['nick'] = run_results.index
                for k in [5,10,20,30]:
                    top_k_results = run_results.head(k)
                    correct_predictions = 0
                    for index, result in top_k_results.iterrows():
                        correct_predictions += self.gold_b[result['nick']]
                    p.append(correct_predictions / k)
                print("PRECISION AT K: =============================")
                print("P@5:"+str(p[0]))
                print("P@10:"+str(p[1]))
                print("P@20:"+str(p[2]))
                print("P@30:"+str(p[3]))
                rank_dit[rank] = {"@5":p[0],"@10":p[1],"@20":p[2],"@30":p[3]}
            else:
                rank_dit[rank] = {"@5":0,"@10":0,"@20":0,"@30":0}
        return rank_dit


############################################################################
class BinaryMultiClassification():
    """ Calculation of metrics for multiclass classification tasks
        Attributes:
            task (str): task to be adressed
            data (DataFrame): table with the sent final prediction. This file has the following structure: 
            gold (Dict): dict with gold labels
    """
    def __init__(self, task: str, data, gold: Dict):
        self.run_results = data 
        self.gold_b, self.gold_multiclass  = read_gold_multiclass(gold)
        self.task = task
    pass

    def penalty(self,delay):
        if self.task == "1": # TCA
            p = 0.0292 # trial
            p = 0.0411 # test
        elif self.task == "2": # Depression
            p = 0.0179 # trial
            p = 0.0326 # test
        else: # Unkown
            p = 0.0308 # test
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
        self.run_results = self.run_results.sort_values(by=['nick'])
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
                        erdes5[ierdes]=1.0 - (1.0/(1.0+np.exp( (r["round"]+1) - 5.0)))
                        erdes30[ierdes]=1.0 - (1.0/(1.0+np.exp( (r["round"]+1) - 30.0)))
                        latency_tps.append(r["round"]+1)
                        penalty_tps.append(self.penalty(r["round"]+1))
                    else: # True negative
                        erdes5[ierdes] = 0
                        erdes30[ierdes] = 0
                else:
                    if ( r['pred_b'] == 1 ): # False positive
                        false_pos+=1
                        erdes5[ierdes]=float(total_pos)/float(len(self.gold_b))
                        erdes30[ierdes]=float(total_pos)/float(len(self.gold_b))
                    else: # False negative
                        erdes5[ierdes]=1
                        erdes30[ierdes]=1
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
        y_true  = list(self.gold_multiclass.values())

        # Binary metrics
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
    

#######################################################################################
class ClassMultiRegressionEvaluation():
    """ Calculation of regression metrics for multi-output regression tasks
        Attributes:
            task (str): task to be adressed
            data (DataFrame): table with the sent final prediction. This file has the following structure: 
            gold (Dict): dict with gold labels
    """
    def __init__(self, task: str, data, gold: Dict):
        self.run_results = data 
        self.gold,self.gold_b = read_gold_multioutput(gold)
        self.task = task

    def eval_performance(self):
        self.run_results = self.run_results.sort_values(by=['nick'])
        y_pred_r = self.run_results['pred'].tolist()
        y_true = list(self.gold.values()) 

        # Regression metrics
        _rmse = metrics.mean_squared_error(y_true, y_pred_r, multioutput='raw_values', squared=False)
        _pearson_sf, _ = pearsonr([item[0] for item in y_true] , [item[0] for item in y_pred_r])
        _pearson_sa, _ = pearsonr([item[1] for item in y_true] , [item[1] for item in y_pred_r])
        _pearson_so, _ = pearsonr([item[2] for item in y_true] , [item[2] for item in y_pred_r])
        _pearson_c, _ = pearsonr([item[3] for item in y_true] , [item[3] for item in y_pred_r])
        rmse = sum(_rmse)/4
        pearson = (_pearson_sf + _pearson_sa + _pearson_so + _pearson_c)/4

        print("REGRESSION METRICS: =============================")
        print("Root Mean Squared Error:")
        print("RMSE mean:"+str(rmse))
        print("RMSE sf:"+str(_rmse[0]))
        print("RMSE sa:"+str(_rmse[1]))
        print("RMSE so:"+str(_rmse[2]))
        print("RMSE c:"+str(_rmse[3]))
        print("Pearson correlation coefficient:")
        print("Pearson mean:"+str(pearson))
        print("Pearson sf:"+str(_pearson_sf))
        print("Pearson sa:"+str(_pearson_sa))
        print("Pearson so:"+str(_pearson_so))
        print("Pearson c:"+str(_pearson_c))

        return { 'RMSE_mean': rmse, 'RMSE_sf': _rmse[0], 'RMSE_sa': _rmse[1], 'RMSE_so': _rmse[2], 'RMSE_c': _rmse[3],'Pearson_mean': pearson,'Pearson_sf': _pearson_sf, 'Pearson_sa': _pearson_sa,'Pearson_so': _pearson_so,'Pearson_c': _pearson_c}

    # Calculation of P@5, P@10, P@20, P@30
    def eval_performance_rank_based(self,results_rank1,results_rank2,results_rank3,results_rank4):
        print("===================================================")
        print("RANK-BASED EVALUATION:")
        results_at=[results_rank1,results_rank2,results_rank3,results_rank4]
        rank_dit = {}
        for results in results_at:
            rank = results.split("_")[-1].split(".")[0]
            print("Analizing ranking at round "+rank)
            p = []
            if os.path.exists(results):
                run_results = pd.read_json(results,orient='index')
                run_results[['suffer+against', 'suffer+in favour', 'suffer+other', 'control']] = run_results['pred'].apply(pd.Series)
                df = run_results.drop('pred', axis=1)
                df0 = df.sort_values(by=['suffer+in favour'],ascending=False)
                df0['nick'] = df0.index
                df1 = df.sort_values(by=['suffer+against'],ascending=False)
                df1['nick'] = df1.index
                df2 = df.sort_values(by=['suffer+other'],ascending=False) 
                df2['nick'] = df2.index
                df3 = df.sort_values(by=['control'],ascending=False) 
                df3['nick'] = df3.index
                for k in [5,10,20,30]:
                    i = 0
                    list_correct_predictions = []
                    for run_results in [df0,df1,df2,df3]:
                        top_k_results = run_results.head(k)
                        correct_predictions = 0
                        for index, result in top_k_results.iterrows():
                            correct_predictions += self.gold_b[result['nick']][i]
                        i += 1
                        list_correct_predictions.append(correct_predictions/k) # Precision at k in one class
                    p.append(sum(list_correct_predictions)/len(list_correct_predictions))
                print("PRECISION AT K: =============================")
                print("P@5:"+str(p[0]))
                print("P@10:"+str(p[1]))
                print("P@20:"+str(p[2]))
                print("P@30:"+str(p[3]))
                rank_dit[rank] = {"@5":p[0],"@10":p[1],"@20":p[2],"@30":p[3]}
            else:
                rank_dit[rank] = {"@5":0,"@10":0,"@20":0,"@30":0}
        return rank_dit

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
    def update_emissions(self,emissions_round):
        # The values are accumulated in each round, so the difference is calculated to know the values for that round only
        if len(emissions_round.items()) != 0:
            if emissions_round['duration'] < 1 :
                return
            if emissions_round['duration'] - self.aux['duration'] < 0 :
                for key, value in self.aux.items():
                    self.aux[key] = 0
            for key, value in self.emissions_run.items():
                if key not in ["cpu_count","gpu_count","cpu_model","gpu_model", "ram_total_size"]:
                    round_ = emissions_round[key] - self.aux[key]
                    self.emissions_run[key].append(round_)
                    self.aux[key] = emissions_round[key]
                else:
                    self.emissions_run[key] = emissions_round[key]
        else:
            for key, value in self.aux.items():
                self.aux[key] = 0

    # Calculation of final values after all predictions have been made
    def calculate_emissions(self):
        dict_ = {}
        for key, value in self.emissions_run.items():
            # Non-numerical values
            if key in ["cpu_count","gpu_count","cpu_model","gpu_model", "ram_total_size"]:
                dict_[key] = self.emissions_run[key]
            # Numerical values
            else:
                dict_[key+"_min"] = min(self.emissions_run[key])
                dict_[key+"_max"] = max(self.emissions_run[key])
                dict_[key+"_mean"] = sum(self.emissions_run[key])/len(self.emissions_run[key])
                dict_[key+"_desv"] = statistics.pstdev(self.emissions_run[key])
        return dict_
