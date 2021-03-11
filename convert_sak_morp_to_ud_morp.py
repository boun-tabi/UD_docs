import sys
import re
import os
import codecs
import fileinput
import argparse


if __name__=="__main__":

   f_filename = sys.argv[1]
   f_morp_filename = sys.argv[2]
   f_new_filename = sys.argv[3]

   f=codecs.open(f_filename, encoding='utf-8', errors='ignore')
   f_morp=codecs.open(f_morp_filename, encoding='utf-8', errors='ignore')
   f_new = codecs.open(f_new_filename, "w", "utf-8")

   morps = f_morp.read()

   morps = morps.split("\n</S> </S>+ESTag\n<S> <S>+BSTag\n")

   

   sak_features = ["A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl", "P1sg", "P2sg", "P3sg", "P1pl", "P2pl", "P3pl", "Abl", "Acc", "Dat", "Equ", "Gen", "Ins", "Loc", "Nom", "Pass", "Caus", "Reflex", "Recip", "Able", "Repeat", "Hastily", "Almost", "Stay", "While", "ByDoingSo", "Pos", "Neg", "Past", "Narr", "Fut", "Aor", "Pres", "Desr", "Cond", "Neces", "Opt", "Imp", "Prog1", "Prog2", "DemonsP", "QuesP", "ReflexP", "PersP", "QuantP", "Card", "Ord", "Distrib", "Ratio", "Range", "Inf", "FutPart", "PastPart", "PresPart"]
  
   ud_features = ["Number=Sing|Person=1", "Number=Sing|Person=2", "Number=Sing|Person=3", "Number=Plur|Person=1", "Number=Plur|Person=2", "Number=Plur|Person=3", "Number[psor]=Sing|Person[psor]=1", "Number[psor]=Sing|Person[psor]=2", "Number[psor]=Sing|Person[psor]=3", "Number[psor]=Plur|Person[psor]=1", "Number[psor]=Plur|Person[psor]=2", "Number[psor]=Plur|Person[psor]=3", "Case=Abl", "Case=Acc", "Case=Dat", "Case=Equ", "Case=Gen", "Case=Ins", "Case=Loc", "Case=Nom", "Voice=Pass", "Voice=Cau", "Voice=Rfl", "Voice=Rcp", "Mood=Abil", "Mood=Iter", "Mood=Rapid", "Mood=Pro", "Mood=Dur", "VerbForm=Conv|Mood=Imp", "VerbForm=Conv|Mood=Imp", "Polarity=Pos", "Polarity=Neg", "Aspect=Perf|Tense=Past|Evident=Fh", "Tense=Past|Evident=Nfh", "Tense=Fut|Aspect=Imp", "Tense=Aor|Aspect=Hab", "Tense=Pres|Aspect=Imp", "Mood=Des", "Mood=Cnd", "Mood=Nec", "Mood=Opt", "Mood=Imp", "Aspect=Prog|Tense=Pres", "Aspect=Prog|Tense=Pres", "PronType=Dem", "PronType=Ind", "PronType=Prs|Reflex=Yes", "PronType=Prs", "PronType=Ind", "NumType=Card", "NumType=Ord", "NumType=Dist", "NumType=Frac", "NumType=Range", "VerbForm=Vnoun", "VerbForm=Part|Tense=Future|Aspect=Imp", "VerbForm=Part|Tense=Past|Aspect=Perf", "VerbForm=Part|Tense=Pres"]

   i = 0
   j = 0
   for line in f:
       line = line.strip()
       
       if len(line) == 0:
          i = i + 1
          j = 0
        

       if len(line) > 0 and not line.startswith('#'):
          
          cols=line.split("\t")
          print(cols)
          print(morps[i].split("\n"))
          if(line == ""):
             print("YES")
          if "[Unknown]" not in morps[i].split("\n")[j].split(" ")[1]:
             
              word = morps[i].split("\n")[j].split(" ")[0]
              morp = morps[i].split("\n")[j].split(" ")[1]

              lemma = morps[i].split("\n")[j].split(" ")[1].split("[")[0]

           
              new_feature_column = []

              for k,feat in enumerate(sak_features):
                  if "["+feat+"]" in morp or "+"+feat+"]" in morp or "["+feat+"+" in morp:
                     new_feature_column.append(ud_features[k])

              new_features_column = list(set(new_feature_column))

              if len(new_features_column) == 0:
                 new_features_column.append("_")

              
              
              new_features = "|".join(new_features_column)

              new_features_arr = new_features.split("|")

              #print(word)
              #print(new_features_arr)

              #exceptional cases
              if "Tense=Past" in new_features_arr and "Tense=Pres" in new_features_arr:
                  new_features_arr.pop(new_features_arr.index("Tense=Pres"))

              if new_features_arr.count("Tense=Past") == 2 and "Evident=Fh" in new_features_arr and "Evident=Nfh" in new_features_arr:
                 new_features_arr.pop(new_features_arr.index("Evident=Nfh"))
                 new_features_arr.pop(new_features_arr.index("Tense=Past"))
                 new_features_arr.pop(new_features_arr.index("Tense=Past"))
                 new_features_arr.append("Tense=Pqb")

              
              delete_list = []
              for k,feat in enumerate(new_features_arr):
                 type = feat.split("=")[0]
                
                 for l in range(k+1,len(new_features_arr)):
                    feat2 = new_features_arr[l]
                    if feat2.startswith(type+"=") and k != l:
                       delete_list.append(k)
                       break

              delete_list.sort(reverse = True)
              for m in delete_list:
                 new_features_arr.pop(m)

             
              feature_vec = "|".join(sorted(new_features_arr))

 
              if feature_vec == "_":
                 cols[5] = cols[5]
              else:
                 if "-" in cols[0]:
                    cols[5] = cols[5]
                 else:
                    cols[5] = feature_vec
                    cols[2] = lemma


          else:
              cols[5] = cols[5] #+"###_"

          j = j + 1
          f_new.write(str(cols[0]+"\t"+cols[1]+"\t"+cols[2]+"\t"+cols[3]+"\t"+cols[4]+"\t"+cols[5]+"\t"+cols[6]+"\t"+cols[7]+"\t"+cols[8]+"\t"+cols[9]+"\n"))
          
       else:
          f_new.write(line+"\n")