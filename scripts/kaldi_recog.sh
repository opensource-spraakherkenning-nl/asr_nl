#!/bin/bash

KALDI_main=??????
KALDI_root=$KALDI_main/egs/wsj/s5
. $KALDI_root/path.sh
. $KALDI_root/utils/parse_options.sh

inputdir=$1
scratchdir=$2
resourcedir=$3
datadir=$2/data
langdir=$3/lang
modeldir=$3/AM
topic=$4
outdir=$5
mkdir -p $datadir
wip="1.0"
iac="11"
frame_shift_opt="--frame-shift=$(cat $modeldir/frame_shift)"

for inputfile in $inputdir/*.wav; do
  file_id=$(basename "$inputfile" .wav)
  echo "$file_id $inputfile" > $datadir/wav.scp
  echo "$file_id spk0000" > $datadir/utt2spk
  echo "spk0000 $file_id" > $datadir/spk2utt
  text=$(cat $inputdir/${file_id}.txt)
  echo "$file_id $text" > $datadir/text

  $KALDI_root/steps/make_mfcc.sh --nj 1 --mfcc-config $model/conf/mfcc.conf $datadir $datadir/log $scratchdir/mfcc
  $KALDI_root/steps/compute_cmvn_stats.sh $datadir $datadir/log $scratchdir/mfcc
  $KALDI_root/steps/online/nnet2/extract_ivectors_online.sh --nj 1 $datadir $resourcedir/ivector_extractor $datadir/ivectors_hires
  $KALDI_root/steps/nnet3/decode.sh --nj 1 --acwt 1.0 --skip-scoring true --post-decode-acwt 10.0 --online-ivector-dir $datadir/ivectors_hires $resourcedir/graph_${topic} $datadir $modeldir/decode_${file_id}
  gunzip -c $modeldir/decode_${file_id}/lat.1.gz \| \
	lattice-push ark:- ark:- \| \
	lattice-add-penalty --word-ins-penalty=$wip ark:- ark:- \| \
	lattice-align-words $langdir/phones/word_boundary.int $model/final.mdl ark:- ark:- \| \
	lattice-to-ctm-conf $frame_shift_opt --inv-acoustic-scale=$iac ark:- - \| $KALDI_root/utils/int2sym.pl -f 5 $langdir/words.txt > $outdir/trans_${file_id} | exit 1;
done
