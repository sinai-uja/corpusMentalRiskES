# MentalRiskES shared task at IberLEF

This repository distributes the data of **MentalRiskES**, the shared task on the early detection of mental disorder risk in Spanish organized at [IberLEF](https://sites.google.com/view/iberlef-2026/) (the Iberian Languages Evaluation Forum, held with the SEPLN conference).

> ⚠️ **Not to be confused with the MentalRiskES corpus.**
> *MentalRiskES* is the name of both this shared task and a dataset of Telegram conversations about eating disorders, depression and anxiety (the [MentalRiskES corpus](https://huggingface.co/datasets/TU_ORG/MentalRiskES), LREC-COLING 2024). The corpus was the data source of the **first two editions** of the shared task (2023 and 2024). The **2025 and 2026 editions use different data** and are unrelated to the corpus.
> The corpus is no longer distributed from this repository: it is available on Hugging Face (see [The MentalRiskES corpus](#the-mentalriskes-corpus)).

## Editions

The task is solved as an online problem: participants receive a continuous stream of messages, organized in rounds, and must detect the risk as early as possible, so systems are evaluated on both accuracy and detection speed.

| Edition (task website) | Venue | Tasks | Data |
|---|---|---|---|
| [2023](https://sites.google.com/view/mentalriskes) | IberLEF 2023 | Task 1: eating disorders detection (1.a binary classification, 1.b simple regression). Task 2: depression detection (2.a binary classification, 2.b simple regression, 2.c multiclass: suffer+against, suffer+in favour, suffer+other, control; 2.d multi-output regression). Task 3: detection of a non-defined disorder, cross-domain evaluation (3.a binary classification, 3.b simple regression) | MentalRiskES corpus |
| [2024](https://sites.google.com/view/mentalriskes2024) | IberLEF 2024 | Task 1: disorder detection (multiclass: depression, anxiety or none). Task 2: context detection (two-level multiclass: disorder plus the context it comes from: addiction, emergency, family, work, social, other or none). Task 3: suicidal ideation detection (binary classification; only test data is provided) | Telegram data from the MentalRiskES corpus |
| [2025](https://sites.google.com/view/mentalriskes2025) | IberLEF 2025 | Task 1: risk detection of gambling disorders (binary classification). Task 2: type of addiction detection (multiclass classification) | PRECOM-SM corpus (gambling in Spanish social media), unrelated to the MentalRiskES corpus |
| [2026](https://sites.google.com/view/mentalriskes2026) | IberLEF 2026 | Task 1: early symptom detection in therapeutic conversations (inferring answers to psychometric instruments: PHQ-9, CompACT-10 and GAP-7). Task 2: therapist response selection (decision support for therapists) | New data, generated and validated with the involvement of psychologists |

## Repository contents

```
.
├── data/
│   ├── mentalriskes2023/
│   │   ├── mentalriskes2023_task1.zip
│   │   ├── mentalriskes2023_task2.zip
│   │   └── mentalriskes2023_task3.zip
│   ├── mentalriskes2024/
│   │   ├── mentalriskes2024_task1.zip
│   │   ├── mentalriskes2024_task2.zip
│   │   └── mentalriskes2024_task3.zip
│   ├── mentalriskes2025/
│   │   ├── mentalriskes2025_task1.zip
│   │   └── mentalriskes2025_task2.zip
│   └── mentalriskes2026/        # TODO: add when the collection is released
├── scripts/
│   ├── MentalRiskES2023/
│   │   ├── classEvaluation.py
│   │   ├── ClientServer.ipynb
│   │   └── CodeCarbon.ipynb
│   └── MentalRiskES2024/
│       ├── classEvaluation.py
│       ├── ClientServer.ipynb
│       └── CodeCarbon.ipynb
├── LICENSE
└── README.md
```

- **`data/`**: the task collections of each edition, one password-protected zip per task (see [Access](#access)).
- **`scripts/`**: the evaluation resources of the editions: the evaluation script (`classEvaluation.py`), the client-server notebook used to simulate the stream of messages round by round (`ClientServer.ipynb`) and the notebook to track the carbon footprint of the systems (`CodeCarbon.ipynb`).

Inside each task zip, the task has the partitions used in the evaluation:

```
<task>/
├── train/
│   ├── data/     # message files (JSON)
│   └── gold/     # labels (txt)
├── trial/
│   ├── data/
│   └── gold/
└── test/
    ├── data/
    └── gold/
```

### File formats

> In the 2024 edition, Task 3 (suicidal ideation detection) provides only test data: participants had to train their systems with their own or external data.

The format below corresponds to the 2023 and 2024 collections.

`data/` contains JSON files with lists of messages:

```json
{
  "id_message": 79865009803,
  "nick": "subject1",
  "round": 1,
  "message": "...",
  "date": "2020-04-07 05:00:02"
}
```

- `nick`: anonymous identifier of the subject.
- `round`: round in which the message is delivered to the participants in the online simulation.

`gold/` contains one or more `.txt` files with the labels of the subjects, in CSV format with the header `Subject,label`. The number of gold files depends on the task: for example, the 2023 Task 2 has four (`gold_a.txt` to `gold_d.txt`), one for each of its subtasks 2.a to 2.d.

```
Subject,label
subject1,1
subject104,0
```

## Access

The collections contain messages written by real users, so access is restricted and granted on an individual basis, only for research purposes.

1. Fill in and sign the [**Individual Application to use the MentalRiskES Research Collection**](https://docs.google.com/forms/d/e/1FAIpQLSfASdCzvR6DCWpFXb4eDpF6gh7CjhJKT1bH2l-SdCcxTP7l7Q/viewform?usp=header), indicating the collection you need (for example `mentalriskes2023_task2` or `mentalriskes2024_task1`).
2. Contact the organizers (see [Contact](#contact)).
3. You will receive the password of the requested zip file(s) after your application is reviewed.

By applying you accept, among others, the following terms (the signed application contains the full text):

- The information may only be used for research purposes.
- You may not identify the individuals whose texts are included, cross-reference them with other data, or contact them.
- You may not publish any portion of the data (e.g. example posts) other than summary statistics, nor share it with anyone else.
- You may not make commercial use of the collection.
- Any publication derived from the collection must cite the corresponding paper(s) (see [Citation](#citation)).
- You must stop using the collection and delete it if the organizers or copyright holders ask you to.

All findings obtained with this data are intended strictly for **non-clinical research**. Individuals in need of professional help are advised to consult licensed psychiatrists or clinicians.

## The MentalRiskES corpus

The corpus of Telegram conversations on which the 2023 and 2024 editions were built is distributed separately, with automated access, as a Hugging Face dataset:

👉 **[huggingface.co/datasets/TU_ORG/MentalRiskES](https://huggingface.co/datasets/amarmol/MentalRiskES)**

It contains the whole corpus (eating disorders, depression and anxiety, with the processed and the raw version of the text), loadable with `load_dataset`. It does **not** contain the train/trial/test partitions of the shared task: those are the collections of this repository.

## Citation

Cite the **overview paper of the edition** you use and, when the edition is built on a dataset with its own paper, **also the data paper**. The table tells you which entries to copy; the BibTeX of each edition is given separately below.

| Edition | Overview paper | Data paper |
|---|---|---|
| [2023](#2023) | `marmol2023overview` | `marmol-romero-etal-2024-mentalriskes-new` (MentalRiskES corpus) |
| [2024](#2024) | `marmol2024overview` | `marmol-romero-etal-2024-mentalriskes-new` (MentalRiskES corpus) |
| [2025](#2025) | `marmol2025overview` | `alvarez2025precom` (PRECOM-SM corpus) |
| [2026](#2026) | `marmol2026overview` | none |

### 2023

Overview of the edition:

```bibtex
@article{marmol2023overview,
  title={Overview of MentalriskES at IberLEF 2023: Early Detection of Mental Disorders Risk in Spanish},
  author={M{\'a}rmol-Romero, Alba Mar{\'\i}a and Moreno-Mu{\~n}oz, Adri{\'a}n and Plaza-del-Arco, Flor Miriam and Molina-Gonz{\'a}lez, Mar{\'\i}a Dolores and Mart{\'\i}n-Valdivia, Maria Teresa and Ure{\~n}a-L{\'o}pez, Luis Alfonso and Montejo-Ra{\'e}z, Arturo},
  journal={Procesamiento del Lenguaje Natural},
  volume={71},
  pages={329--350},
  year={2023}
}
```

Data: the [MentalRiskES corpus](#the-mentalriskes-corpus):

```bibtex
@inproceedings{marmol-romero-etal-2024-mentalriskes-new,
  title = "{M}ental{R}isk{ES}: A New Corpus for Early Detection of Mental Disorders in {S}panish",
  author = "M{\'a}rmol-Romero, Alba Mar{\'\i}a and Moreno-Mu{\~n}oz, Adri{\'a}n and Plaza-del-Arco, Flor Miriam and Molina-Gonz{\'a}lez, M. Dolores and Mart{\'\i}n-Valdivia, Mar{\'\i}a Teresa and Ure{\~n}a-L{\'o}pez, L. Alfonso and Montejo-R{\'a}ez, Arturo",
  booktitle = "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)",
  month = may,
  year = "2024",
  address = "Torino, Italia",
  publisher = "ELRA and ICCL",
  url = "https://aclanthology.org/2024.lrec-main.978",
  pages = "11204--11214"
}
```

### 2024

Overview of the edition:

```bibtex
@article{marmol2024overview,
  title={Overview of MentalriskES at IberLEF 2024: Early Detection of Mental Disorders Risk in Spanish},
  author={M{\'a}rmol-Romero, Alba Mar{\'\i}a and Moreno-Mu{\~n}oz, Adri{\'a}n and Plaza-del-Arco, Flor Miriam and Molina-Gonz{\'a}lez, Mar{\'\i}a Dolores and Mart{\'\i}n-Valdivia, Maria Teresa and Ure{\~n}a-L{\'o}pez, Luis Alfonso and Montejo-Ra{\'e}z, Arturo},
  journal={Procesamiento del Lenguaje Natural},
  volume={73},
  pages={435--448},
  year={2024}
}
```

Data: the [MentalRiskES corpus](#the-mentalriskes-corpus):

```bibtex
@inproceedings{marmol-romero-etal-2024-mentalriskes-new,
  title = "{M}ental{R}isk{ES}: A New Corpus for Early Detection of Mental Disorders in {S}panish",
  author = "M{\'a}rmol-Romero, Alba Mar{\'\i}a and Moreno-Mu{\~n}oz, Adri{\'a}n and Plaza-del-Arco, Flor Miriam and Molina-Gonz{\'a}lez, M. Dolores and Mart{\'\i}n-Valdivia, Mar{\'\i}a Teresa and Ure{\~n}a-L{\'o}pez, L. Alfonso and Montejo-R{\'a}ez, Arturo",
  booktitle = "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)",
  month = may,
  year = "2024",
  address = "Torino, Italia",
  publisher = "ELRA and ICCL",
  url = "https://aclanthology.org/2024.lrec-main.978",
  pages = "11204--11214"
}
```

### 2025

Overview of the edition:

```bibtex
@article{marmol2025overview,
  title={Overview of MentalRiskES at IberLEF 2025: Early Detection of Addiction Risk in Spanish},
  author={M{\'a}rmol-Romero, Alba Mar{\'\i}a and {\'A}lvarez-Ojeda, Pablo and Moreno-Mu{\~n}oz, Adri{\'a}n and Plaza-del-Arco, Flor Miriam and Molina-Gonz{\'a}lez, M. Dolores and Mart{\'\i}n-Valdivia, M. Teresa and Ure{\~n}a-L{\'o}pez, L. Alfonso and Montejo-R{\'a}ez, Arturo},
  journal={Procesamiento del Lenguaje Natural},
  volume={75},
  pages={425--440},
  year={2025}
}
```

Data: the PRECOM-SM corpus (gambling in Spanish social media). It is a different resource from the MentalRiskES corpus:

```bibtex
@inproceedings{alvarez2025precom,
  title={The precom-sm corpus: Gambling in spanish social media},
  author={{\'A}lvarez-Ojeda, Pablo and Cantero-Romero, Mar{\'\i}a Victoria and Semikozova, Anastasia and Montejo-R{\'a}ez, Arturo},
  booktitle={Proceedings of the 31st International Conference on Computational Linguistics},
  pages={17--28},
  year={2025}
}
```

### 2026

Overview of the edition (the data were created for this edition):

```bibtex
@article{marmol2026overview,
  title={Overview of MentalRiskES at IberLEF 2026: Early Detection of Mental Disorders Risk in Spanish},
  author={M{\'a}rmol-Romero, Alba Mar{\'\i}a and Su{\'a}rez-Maroto, Fabi{\'a}n and Garc{\'\i}a-Viedma, Rosario and Hern{\'a}ndez-L{\'o}pez, M{\'o}nica and Plaza-del-Arco, Flor Miriam and Molina-Gonz{\'a}lez, M. Dolores and Ure{\~n}a-L{\'o}pez, L. Alfonso and Montejo-R{\'a}ez, Arturo},
  journal={Procesamiento del Lenguaje Natural},
  volume={77},
  month=sep,
  year={2026}
}
```

## Contact

To request access or ask about the collections:

- Alba M. Mármol Romero (amarmol@ujaen.es)
- Arturo Montejo Ráez (amontejo@ujaen.es)
