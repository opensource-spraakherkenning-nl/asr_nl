#!/bin/bash

if [[ $(hostname) == "mlp01" ]]; then
    KALDI_main=/var/www/lamachine/src/kaldi
elif [[ $(hostname) == "applejack" ]]; then
    KALDI_main=/vol/customopt/kaldi
elif [[ $(hostname) == "mlp11" ]]; then
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
for inputfile in $inputdir/*; do

  filename=$(basename "$inputfile")
  extension="${filename##*.}"
  file_id=$(basename "$inputfile" .$extension)
  sox $inputfile -e signed-integer -c 1 -r 16000 -b 16 $scratchdir/${file_id}.wav
  target_dir=$scratchdir/${file_id}_$(date +"%y_%m_%d_%H_%m_%S")
  mkdir -p $target_dir

  if [[ "$topic" == "GN" ]]; then
    ./decode.sh $scratchdir/${file_id}.wav $target_dir
  elif [[ "$topic" == "OH" ]]; then
    ./decode_OH.sh $scratchdir/${file_id}.wav $target_dir
  elif [[ "$topic" == "PR" ]]; then
    ./decode_PR.sh $scratchdir/${file_id}.wav $target_dir
  fi

  cat $target_dir/${file_id}.txt | cut -d'(' -f 1 > $outdir/${file_id}.txt
  cp $target_dir/1Best.ctm $outdir/${file_id}.ctm
  ./scripts/ctm2xml.py $outdir $file_id $scratchdir

  # Create .rttm
  spkr_seg=$target_dir/liumlog/${file_id}.seg
  cat $spkr_seg | sed -n '/;;/!p' | sort -nk3 | awk '{printf "SPEAKER %s %s %.2f %.2f <NA> <NA> %s <NA>\n", $1, $2, ($3 / 100), ($4 / 100), $8}' > $outdir/${file_id}.rttm

  # Create .ctm with speaker ids
  ./scripts/ctm2xml.py $outdir/${file_id}.rttm $outdir/${file_id}.ctm

  # Add sentence boundaries
  cat $outdir/${file_id}.ctm | perl scripts/wordpausestatistic.perl 1.0 $outdir/${file_id}.sent


done
cd -
