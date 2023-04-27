#!/bin/sh

: ${mph=%mph%}
Verbose=0
Config=0
while :
do case "x$1" in
       x-v) Verbose=1
	    shift
	    ;;
       x-c) Config=1
	    shift
	    ;;
       x-h) cat >&2 <<'!'
Usage: bio [-v] [-c] k1 mu time
MSolve simulation of tumor grouth
   k1       growth rate, 1/second
   mu       shear modulus, kPa
   time     timestep in days (positive integer)
Options:
  -v        verbose output
  -c        output MSolve confiuration file and exit
  -h        display help and exit
!
	    exit 2
	    ;;
       x-*) printf >&2 'bio: error: unknown option %s' "$1"
	    exit 2
	    ;;
       *) break
	  ;;
   esac
done

case $# in
    3) k1=$1; mu=$2; time=$3 ;;
    *) printf >&1 'bio: error: needs three arguments\n'
       exit 2
       ;;
esac

case "$time" in
    [1-9]*) ;;
    *) echo 'bio: error: time should be an positive integer' >&2; exit 2;;
esac

if ! test -f "$mph"
then printf "bio: error: cannot find mesh '%s'\n" "$mph" >&2
     exit 2
fi
c=/tmp/config.$$.xml
r=/tmp/result.$$.xml
trap 'rm -f $c $r; exit 2' 1 2 15
cat <<! > $c
<MSolve4Korali version="1.0">
        <Mesh>
                <File>$mph</File>
        </Mesh>
        <Physics type="TumorGrowth">
                <Time>$time</Time>
                <Timestep>1</Timestep>
        </Physics>
        <Output>
                <TumorVolume/>
        </Output>
        <Parameters>
                <k1>$k1</k1>
                <mu>$mu</mu>
        </Parameters>
</MSolve4Korali>
!

case $Config in
    0) if ! command >/dev/null -v ISAAR.MSolve.MSolve4Korali
       then
	   echo 'bio: ISAAR.MSolve.MSolve4Korali command is not avialabe' >&2
	   exit 2
       fi
       case $Verbose in
	   0) ISAAR.MSolve.MSolve4Korali 2>/dev/null 1>/dev/null $c $r ;;
	   1) ISAAR.MSolve.MSolve4Korali 1>&2 $c $r ;;
       esac
       rc=$?
       case $rc in
	   0)  if ! awk -v RS='\r\n' 'sub(/^[ \t]*<SolutionMsg>/, "") && sub(/<\/SolutionMsg>[ \t]*/, "") && /^Success$/ {exit 1}' $r
	       then
		   awk -v RS='\r\n' 'sub(/^[ \t]*<Volume>/, "") && sub(/<\/Volume>[ \t]*/, "")' $r
	       else
		   echo Fail
	       fi
	       ;;
	   *) echo Fail ;;
       esac
       ;;
    1) cat $c
       ;;
esac
case $Verbose in
    0) rm -f $c $r
       ;;
esac
exit $rc
