Strong scaling

```
for n in 1 2 4 8 12 16 24; do python3 bio0.py -d 48 -n $n -s; done | tee log
```

Weak scaling

```
for n in 1 2 4 8 12 16 24
do d=`echo $n | awk '{print 24 * $n}'`
   python3 bio0.py -d $d -n $n -s; done  | tee log
```
