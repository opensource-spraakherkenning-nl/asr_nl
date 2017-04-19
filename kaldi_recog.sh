#!/bin/bash

if [[ $(hostname) == "applejack" ]]; then
    KALDI_main=/vol/customopt/kaldi
elif [[ $(hostname) == "twist" ]]; then
    KALDI_main=/vol/customopt/kaldi
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
  target_dir=$scratchdir/${file_id}_$(date -d "today" +"%Y%m%d%H%M")
  mkdir -p $target_dir
  ./decode.sh $inputfile $target_dir
  cat $target_dir/${file_id}.txt | cut -d'(' -f 1 > $outdir/${file_id}.txt
  rm -rf $target_dir
done
cd -
