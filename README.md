# MentalRiskES
MentalRiskES is a new dataset about mental disorders in Spanish. The dataset is divided into three distinct mental disorders:
- Eating Disorder
- Depression
- Anxiety
  
Each dataset comprises a set of subjects and their corresponding message threads from a Telegram social network chat.

## How is it constructed? 🛠️
Public groups on the [Telegram social network](https://telegram.org/) were accessed, and conversations were extracted from them. This data was processed, and we retained only the text messages, excluding images, audio, and other media. 
In order to carry out the annotation, a subset of messages was extracted from each subject. This message thread was annotated by 10 different annotators through the [Prolific platform](https://www.prolific.com/) and made use of the [Doccano annotation platform](https://github.com/doccano/doccano).

In this way, we associated a user ID with some tags that emerged after averaging the annotators' decisions. The labels available for each set are:
- Eating Disorder: suffer (s), control (c)
- Depression: suffer + in favour (sf), suffer + against (sa), suffer + other (so), control (c)
- Anxiety: suffer (s), control (c)
  
### Annotation guides 📄
Each corpus has an annotation guide adapted to its case. It is accompanied by a user manual for a better understanding of the annotation platform. Links to the annotation guides are provided below:
- [Annotation Guide for the Anxiety corpus](https://drive.google.com/file/d/1wpJBWu4mNEw9bmSkX089G67TfNzSkjKX/view?usp=sharing)
- [Annotation Guide for the Depression corpus](https://drive.google.com/file/d/10-18MqgbKhQ91QyhUFOzYsfIugAfBu01/view?usp=drive_link)
- [Annotation Guide for the Eating Disorder corpus](https://drive.google.com/file/d/1RwZrQgcXs5ZwLwa-F-b38UvsnfHYQuzM/view?usp=drive_link)

The most predominant label among the annotators is taken, being 1 equal to suffers and 0 equal to does not suffer. In case of a tie, the subject is taken as suffering.

### Labels 🔴🟢
The values available in Anxiety files are:
- bs (binary suffer): 1 if the subject suffers and 0 if not, according to the frequency of the labels (in case of a tie, it is marked as suffers)
- bc (binary control): 1 if the subject does not suffer and 0 if they d,o according to the frequency of the labels (in case of a tie, it is marked as suffers)
- rbs (regression binary suffer): number of times the subject has been marked as suffering among the total number of scorers, i.e., 10
- rbc (regression binary control): number of times the subject has been marked as not suffering among the total number of scorers, i.e., 10

The values available in the Depression and EatingDisorders files are: 
- bs (binary suffer): 1 if the subject suffers and 0 if not, according to the frequency of the labels (in case of a ti,e it is marked as suffers)
- bsf (binary suffer favour): 1 if the subject suffers and is in favour, and 0 if not, according to the frequency of the labels
- bsa (binary suffer against): 1 if the subject suffers and is agains,t and 0 if not, according to the frequency of the labels
- bso (binary suffer other):  1 if the subject suffers and is neither in favour nor against, and 0 if not, according to the frequency of the labels
- bc (binary control): 1 if the subject does not suffer and 0 if they do, according to the frequency of the labels (in case of a ti,e it is marked as suffers)
- rbs (regression binary suffer): number of times the subject has been marked as suffering among the total number of scorers, i.e., 10
- rbc (regression binary control): number of times the subject has been marked as not suffering among the total number of scorers, i.e., 10
- rsf (regression suffer favour): number of times the subject has been marked as suffering and in favour among the total number of scorers, i.e., 10
- rsa (regression suffer against): number of times the subject has been marked as suffering and against and in favour among the total number of scorers, i.e., 10
- rso (regression suffer other): number of times the subject has been marked as suffering and is neither in favour nor against among the total number of scorers, i.e., 10
- rc (regression control): number of times the subject has been marked as not suffering among the total number of scorers, i.e., 10 (Note that it is equal to 'rbc')

So, the labels 'rbs' and 'rbc' must sum to 1, and the labels 'rsf', 'rsa', 'rso' and 'rc' must sum to 1 too.

### Preprocessing 🧹
The same corpus is found with emojis or without emojis; that is to say, in the folder 'processed' is the corpus with emojis in text format, while in the folder 'raw' is the corpus with emojis in original format.

### MentalRiskES evaluation campaign 🚀
[MentalRiskES](https://sites.google.com/view/mentalriskes) is a shared task organized at IberLEF. This task aims to promote the early detection of mental risk disorders in Spanish. In this task, we used the corpusMentalRiskES; the partitions used are available in the folder MentalRiskES2023edition.zip. To cite the task: 
Mármol-Romero, A. M., Moreno-Muñoz, A., Plaza-del-Arco, F. M., Molina-González, M. D., Martín-Valdivia, M. T., Ureña-López, L. A., & Montejo-Raéz, A. (2023). Overview of MentalriskES at IberLEF 2023: Early Detection of Mental Disorders Risk in Spanish. Procesamiento del Lenguaje Natural, 71, 329-350.
```
@article{marmol2023overview,
  title={Overview of MentalriskES at IberLEF 2023: Early Detection of Mental Disorders Risk in Spanish},
  author={M{\'a}rmol-Romero, Alba Mar{\'\i}a and Moreno-Mu{\~n}oz, Adri{\'a}n and Plaza-del-Arco, Flor Miriam and Molina-Gonz{\'a}lez, Mar{\'\i}a Dolores and Mart{\'\i}n-Valdivia, Maria Teresa and Ure{\~n}a-L{\'o}pez, Luis Alfonso and Montejo-Ra{\'e}z, Arturo},
  journal={Procesamiento del Lenguaje Natural},
  volume={71},
  pages={329--350},
  year={2023}
}
```
Mármol-Romero, A. M., Moreno-Muñoz, A., Plaza-del-Arco, F. M., Molina-González, M. D., Martín-Valdivia, M. T., Ureña-López, L. A., & Montejo-Raéz, A. (2024). Overview of MentalriskES at IberLEF 2024: Early Detection of Mental Disorders Risk in Spanish. Procesamiento del Lenguaje Natural, 73, 435-448.
```
@article{marmol2024overview,
  title={Overview of MentalriskES at IberLEF 2024: Early Detection of Mental Disorders Risk in Spanish},
  author={M{\'a}rmol-Romero, Alba Mar{\'\i}a and Moreno-Mu{\~n}oz, Adri{\'a}n and Plaza-del-Arco, Flor Miriam and Molina-Gonz{\'a}lez, Mar{\'\i}a Dolores and Mart{\'\i}n-Valdivia, Maria Teresa and Ure{\~n}a-L{\'o}pez, Luis Alfonso and Montejo-Ra{\'e}z, Arturo},
  journal={Procesamiento del Lenguaje Natural},
  volume={73},
  pages={435--448},
  year={2024}
}
```

## Zenodo 📂
Dataset: 10.5281/zenodo.8055604 (DOI)

## Ethics Statement ⭐
The main purpose of creating this dataset is to provide a tool for developing systems with scientific aims and advancing artificial intelligence to detect mental disorders among young people on social networks at an early stage. The data has been labelled using measures to ensure gender diversity and avoid discrimination through our annotation platform. It's important to emphasize that all findings from this dataset are intended strictly for non-clinical research. Individuals in need of professional help are advised to consult licensed psychiatrists or clinicians.

## Contact 📩
To request access to the corpus, please fill this [form](https://docs.google.com/forms/d/e/1FAIpQLSfASdCzvR6DCWpFXb4eDpF6gh7CjhJKT1bH2l-SdCcxTP7l7Q/viewform?usp=header) and then contact:
- Alba M. Mármol Romero (amarmol@ujaen.es)
- Arturo Montejo Ráez (amontejo@ujaen.es)

## Acknowledgements 
This work has been partially supported by projects CONSENSO (PID2021-122263OB-C21), MODERATES (TED2021-130145B-I00), SocialTOX (PDC2022-133146-C21) funded by Plan Nacional I+D+i from the Spanish Government, project PRECOM (SUBV-00016) funded by Spanish Ministry of Consumer Affairs, and the Big Hug project (P20\_00956, PAIDI 2020), funded by the Andalusian Regional Government.

## Citation of the corpus ❗
Mármól-Romero, A. M., Moreno-Muñoz, A., Plaza-del-Arco, F. M., Molina-González, M. D., Martín-Valdivia, M. T., Ureña-López, L. A., & Montejo-Ráez, A. (2024). MentalRiskES: A new corpus for early detection of mental disorders in Spanish. En N. Calzolari, M.-Y. Kan, V. Hoste, A. Lenci, S. Sakti & N. Xue (Eds.), Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024) (pp. 11204–11214). ELRA and ICCL. 
https://aclanthology.org/2024.lrec-main.978

```
@inproceedings{marmol-romero-etal-2024-mentalriskes-new,
    title = "{M}ental{R}isk{ES}: A New Corpus for Early Detection of Mental Disorders in {S}panish",
    author = "M{\'a}rmol-Romero, Alba Mar{\'\i}a  and
      Moreno-Mu{\~n}oz, Adri{\'a}n  and
      Plaza-del-Arco, Flor Miriam  and
      Molina-Gonz{\'a}lez, M. Dolores  and
      Mart{\'\i}n-Valdivia, Mar{\'\i}a Teresa  and
      Ure{\~n}a-L{\'o}pez, L. Alfonso  and
      Montejo-R{\'a}ez, Arturo",
    editor = "Calzolari, Nicoletta  and
      Kan, Min-Yen  and
      Hoste, Veronique  and
      Lenci, Alessandro  and
      Sakti, Sakriani  and
      Xue, Nianwen",
    booktitle = "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)",
    month = may,
    year = "2024",
    address = "Torino, Italia",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.lrec-main.978",
    pages = "11204--11214",
    abstract = "With mental health issues on the rise on the Web, especially among young people, there is a growing need for effective identification and intervention. In this paper, we introduce a new open-sourced corpus for the early detection of mental disorders in Spanish, focusing on eating disorders, depression, and anxiety. It consists of user messages posted on groups within the Telegram message platform and contains over 1,300 subjects with more than 45,000 messages posted in different public Telegram groups. This corpus has been manually annotated via crowdsourcing and is prepared for its use in several Natural Language Processing tasks including text classification and regression tasks. The samples in the corpus include both text and time data. To provide a benchmark for future research, we conduct experiments on text classification and regression by using state-of-the-art transformer-based models.",
}

```
