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
topic=$4

cd $KALDI_root
for inputfile in $inputdir/*.wav; do
  file_id=$(basename "$inputfile" .wav)
  sox $inputfile -e signed-integer -r 16000 -b 16 $scratchdir/${file_id}.wav
  target_dir=$scratchdir/${file_id}_$(date +"%y_%m_%d_%H_%m_%S")
  mkdir -p $target_dir
  if [[ "$topic" == "GN" ]]; then
    ./decode.sh $scratchdir/${file_id}.wav $target_dir
  elif [[ "$topic" == "OH" ]]; then
    ./decode_OH.sh $scratchdir/${file_id}.wav $target_dir
  fi
  cat $target_dir/${file_id}.txt | cut -d'(' -f 1 > $outdir/${file_id}.txt
  cp $target_dir/1Best.ctm $outdir/${file_id}.ctm
  ./scripts/ctm2xml.py $outdir $file_id $scratchdir
done
cd -
