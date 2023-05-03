#!/bin/sh



inputdir=$1
scratchdir=$2
outdir=$3
resourcedir=$4
topic=$5
debug=$6

echo "Input directory: $inputdir" >&2
echo "Scratch directory: $scratchdir" >&2
echo "Output directory: $outdir" >&2
echo "Resource directory: $resourcedir" >&2

fatalerror() {
    echo "-----------------------------------------------------------------------" >&2
    echo "FATAL ERROR: $*" >&2
    echo "-----------------------------------------------------------------------" >&2
    rm "$scratchdir/${file_id}.wav" 2>/dev/null
    if [ -n "$target_dir" ]; then
        echo "PATH=$PATH" >&2
        echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH" >&2
        echo "KALDI_ROOT=$KALDI_ROOT" >&2
        echo "[Index of $target_dir]" >&2
        du -ah "$target_dir" >&2
        echo "[End of index]">&2
        echo "[Output of intermediate log]" >&2
        cat "$target_dir/intermediate/log" >&2
        echo "[End output of intermediate log]">&2
        echo "[Output of intermediate lium logs]" >&2
        cat "$target_dir"/intermediate/data/ALL/liumlog/*.log >&2
        echo "[End output of intermediate log]">&2
        echo "[Output of other intermediate logs]" >&2
        cat "$target_dir"/intermediate/data/ALL/log/*.log >&2
        echo "[End output of other intermediate log]">&2
        echo "[Output of kaldi decode logs]" >&2
        cat "$target_dir"/intermediate/decode/log/decode*log >&2
        echo "[End of kaldi decode logs]" >&2
        if [ -n "$debug" ]; then
            echo "(cleaning intermediate files after error)">&2
            rm -Rf "$target_dir"
        fi
    fi
    exit 2
}

if [ -z "$topic" ]; then
    topic="OH"
fi

cd "$resourcedir" || fatalerror "Resourcedir not found"
for inputfile in "$inputdir"/*; do

  echo "Processing $inputfile" >&2
 
  extension="${inputfile##*.}"
  file_id=$(basename "$inputfile" ."$extension" | sed 's/[^a-zA-Z0-9\.\-]/_/g')
  ffmpeg -i "$inputfile" -sample_fmt s16 -ac 1 -ar 16000 "$scratchdir/${file_id}.wav" || fatalerror "Failure calling ffmpeg"

  target_dir="$scratchdir/${file_id}_$(date +"%y_%m_%d_%H_%M_%S_%N")"
  mkdir -p "$target_dir" || fatalerror "Unable to create temporary working directory $target_dir"

  case "$topic" in
      "GN"|"OH"|"PR"|"BD")
        ./"decode_$topic.sh" "$scratchdir/${file_id}.wav" "$target_dir" || fatalerror "Decoding failed ($topic)"
        ;;
      *)
        fatalerror "Unknown topic ($topic)"
        ;;
  esac

  if [ ! -f "$target_dir/${file_id}.txt" ]; then
      fatalerror "Expected target file $target_dir/${file_id}.txt not found after decoding!"
  fi

  if [ ! -f "$target_dir/1Best.ctm" ]; then
      fatalerror "Expected CTM file $target_dir/1Best.ctm not found after decoding!"
  fi


  #strip scores
  cut -d'(' -f 1 "$target_dir/${file_id}.txt" > "$outdir/${file_id}.txt"

  cp "$target_dir/1Best.ctm" "$outdir/${file_id}.ctm"
  cp "$target_dir/1Best.ctm.spk" "$outdir/${file_id}.ctm.spk"
  cp "$target_dir/${file_id}.xml" "$outdir/${file_id}.xml"
  cp "$target_dir/1Best.rttm" "$outdir/${file_id}.rttm"
  cp "$target_dir/1Best.sent" "$outdir/${file_id}.sent"

  #cleanup
  echo "(cleaning intermediate files)">&2
  rm "$scratchdir/${file_id}.wav" 2>/dev/null
  rm -Rf "$target_dir"

done
cd - || exit
