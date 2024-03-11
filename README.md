# MentalRiskEs
MentalRiskEs is a new dataset about mental disorders in Spanish. The dataset is divided into three distinct mental disorders:
- Eating Disorder
- Depression
- Anxiety
  
Each dataset contains a set of subjects and their message thread in a Telegram social network chat.

## How is constructed?

Public groups on the [Telegram social network](https://telegram.org/) were accessed and conversations were extracted from them. This data was processed and we kept only the text messages, excluding images, audio, etc. 
In order to carry out the annotation, a subset of messages was extracted from each subject. This message thread was annotated by 10 different annotators through the [Prolific platform](https://www.prolific.com/) and made use of the [Doccano annotation platform](https://github.com/doccano/doccano).

In this way, we associated a user ID with some tags that emerged after averaging the annotators' decisions. The labels available for each set are:
- Eating Disorder: suffer (s), control (c)
- Depression: suffer + in favour (sf), suffer + against (sa), suffer + other (so), control (c)
- Anxiety: suffer (s), control (c)
  
### Annotation guides
Each corpus has an annotation guide adapted to its case. It is accompanied by a user manual for a better understanding of the annotation platform. Links to the annotation guides are provided below:
- [Annotation Guide for the Anxiety corpus](https://drive.google.com/file/d/1wpJBWu4mNEw9bmSkX089G67TfNzSkjKX/view?usp=sharing)
- [Annotation Guide for the Depression corpus](https://drive.google.com/file/d/10-18MqgbKhQ91QyhUFOzYsfIugAfBu01/view?usp=drive_link)
- [Annotation Guide for the Eating Disorder corpus](https://drive.google.com/file/d/1RwZrQgcXs5ZwLwa-F-b38UvsnfHYQuzM/view?usp=drive_link)

The most predominant label among the annotators is taken, being 1 equal to suffers and 0 equal to does not suffer. In case of a tie, the subject is taken as suffering.

### Labels
The values available in Anxiety files are:
- bs (binary suffer): 1 if the subject suffers and 0 if not according to the frequency of the labels (in case of a tie it is marked as suffers)
- bc (binary control): 1 if the subject does not suffer and 0 if they do according to the frequency of the labels (in case of a tie it is marked as suffers)
- rbs (regression binary suffer): number of times the subject has been marked as suffering among the total number of scorers, i.e., 10
- rbc (regression binary control): number of times the subject has been marked as not suffering among the total number of scorers, i.e., 10

The values available in Depression and EatingDisorders files are: 
- bs (binary suffer): 1 if the subject suffers and 0 if not according to the frequency of the labels (in case of a tie it is marked as suffers)
- bsf (binary suffer favour): 1 if the subject suffers and is in favour and 0 if not according to the frequency of the labels
- bsa (binary suffer against): 1 if the subject suffers and is against and 0 if not according to the frequency of the labels
- bso (binary suffer other):  1 if the subject suffers and is neither in favour nor against and 0 if not according to the frequency of the labels
- bc (binary control): 1 if the subject does not suffer and 0 if they do according to the frequency of the labels (in case of a tie it is marked as suffers)
- rbs (regression binary suffer): number of times the subject has been marked as suffering among the total number of scorers, i.e., 10
- rbc (regression binary control): number of times the subject has been marked as not suffering among the total number of scorers, i.e., 10
- rsf (regression suffer favour): number of times the subject has been marked as suffering and in favour among the total number of scorers, i.e., 10
- rsa (regression suffer against): number of times the subject has been marked as suffering and against and in favour among the total number of scorers, i.e., 10
- rso (regression suffer other): number of times the subject has been marked as suffering and is neither in favour nor against among the total number of scorers, i.e., 10
- rc (regression control): number of times the subject has been marked as not suffering among the total number of scorers, i.e., 10 (Note that it is equal to 'rbc')

So, the labels 'rbs' and 'rbc' must sum to 1, and the labels 'rsf','rsa', 'rso' and 'rc' must sum to 1 too.

### Preprocessing
The same corpus is found with emojis or without emojis, that is to say, in the folder 'processed' is the corpus with emojis in text format while in the folder 'raw' is the corpus with emojis in original format.



