#!/bin/bash


fatalerror() {
    echo "$*" >&2
    rm $scratchdir/${file_id}.wav 2>/dev/null
    exit 2
}

inputdir=$1
scratchdir=$2
outdir=$3
resourcedir=$4
topic=$5

echo "Input directory: $inputdir" >&2
echo "Scratch directory: $scratchdir" >&2
echo "Output directory: $outdir" >&2
echo "Resource directory: $resourcedir" >&2

cd $resourcedir
for inputfile in $inputdir/*; do
  filename=$(basename "$inputfile")
  echo "Processing $filename" >&2
  extension="${filename##*.}"
  file_id=$(basename "$inputfile" .$extension)
  sox $inputfile -e signed-integer -c 1 -r 16000 -b 16 $scratchdir/${file_id}.wav || fatalerror "Failure calling sox"
  target_dir=$scratchdir/${file_id}_$(date +"%y_%m_%d_%H_%m_%S")
  mkdir -p $target_dir

  if [[ "$topic" == "GN" ]]; then
    ./decode.sh $scratchdir/${file_id}.wav $target_dir || fatalerror "Decoding failed (GN)"
  elif [[ "$topic" == "OH" ]]; then
    ./decode_OH.sh $scratchdir/${file_id}.wav $target_dir || fatalerror "Decoding failed (OH)"
  elif [[ "$topic" == "PR" ]]; then
    ./decode_PR.sh $scratchdir/${file_id}.wav $target_dir || fatalerror "Decoding failed (PR)"
  fi

  if [ -f $target_dir/${file_id}.txt ]; then
      fatalerror "Expected target file $target_dir/${file_id}.txt not found!"
  fi

  cat $target_dir/${file_id}.txt | cut -d'(' -f 1 > $outdir/${file_id}.txt
  cp $target_dir/1Best.ctm $outdir/${file_id}.ctm
  ./scripts/ctm2xml.py $outdir $file_id $scratchdir || fatalerror "ctm2xml failed"

  # Create .rttm
  spkr_seg=$target_dir/liumlog/${file_id}.seg
  cat $spkr_seg | sed -n '/;;/!p' | sort -nk3 | awk '{printf "SPEAKER %s %s %.2f %.2f <NA> <NA> %s <NA>\n", $1, $2, ($3 / 100), ($4 / 100), $8}' > $outdir/${file_id}.rttm

  # Create .ctm with speaker ids
  ./scripts/addspkctm.py $outdir/${file_id}.rttm $outdir/${file_id}.ctm || fatalerror "Failure calling addspkctm.py"

  # Add sentence boundaries
  cat $outdir/${file_id}.ctm | perl scripts/wordpausestatistic.perl 1.0 $outdir/${file_id}.sent

  #cleanup
  rm $scratchdir/${file_id}.wav 2>/dev/null

done
cd -
