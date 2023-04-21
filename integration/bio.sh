#!/bin/sh

: ${mph=%mph%}
usage () {
    echo 'Usage: bio [-v] [-h] k1 mu time' >&2
    exit 1
}

case "$1" in
    -v) Verbose=1; shift ;;
    -h) usage ;;
    *) Verbose=0 ;;
esac

case $# in
    3) k1=$1; mu=$2; time=$3 ;;
    *) usage ;;
esac

case "$time" in
    [1-9]*) ;;
    *) echo 'bio: time should be an positive integer' >&2; exit 1;;
esac

if ! test -f "$mph"
then printf "bio: cannot find mesh '%s'\n" "$mph" >&2
     exit 1
fi
c=/tmp/config.$$.xml
r=/tmp/result.$$.xml
trap 'rm -f $c $r; exit 1' 1 2 15
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

if ! command >/dev/null -v ISAAR.MSolve.MSolve4Korali
then
    echo 'bio: ISAAR.MSolve.MSolve4Korali command is not avialabe' >&2
    exit 1
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
case $Verbose in
    0) rm -f $c $r ;;
    *) ;;
esac
exit $rc