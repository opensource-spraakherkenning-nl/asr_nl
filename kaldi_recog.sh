#!/bin/bash

if [[ $(hostname) == "applejack" ]]; then
    KALDI_main=/vol/customopt/kaldi
elif [[ $(hostname) == "twist" ]]; then
    KALDI_main=/vol/tensusers/eyilmaz/kaldi
else
    echo "Specify KALDI_main!" >&2
    exit 2
fi
KALDI_root=$KALDI_main/egs/Kaldi_NL
inputdir=$1
scratchdir=$2
outdir=$3

cd $KALDI_root
for inputfile in $inputdir/*.wav; do
  file_id=$(basename "$inputfile" .wav)
  ./decode.sh $inputfile $scratchdir
  cp $scratchdir/${file_id}.txt $outdir/${file_id}.txt
done
cd -
