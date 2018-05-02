# this scripts takes a KALDI ctm file as input (on stdin)
# and spits out the sequence of hypotheses in the form of a list of sequences
# in file tmp in current directory

# argument: pause duration threshold [1 sec]

$thr1 = 0.8;
$thr2 = 1;

if ($#ARGV >= 0)
  {
  $thr2 = $ARGV[0];
  $output = $ARGV[1];
  }



open(OUT, ">" . $output);


while (<stdin>)
  {
  chomp;
  @tok = split(/\s+/);
  $onset = $tok[2];
  $dur = $tok[3];
  $word = $tok[4];
  $m0++;
  $m1 += $dur;
  $m2 += ($dur)*($dur);
  $durarray{$.} = $dur;
  $wordarray{$.} = $word;
  $onsetarray{$.} = $onset;
  }
$nrinputs = $.;

#printf(OUT "%d %f %f\n", $m0, $m1, $m2);

$current_sentence = "";

for ($j = 0; $j <= $nrinputs; $j++)
  {
  #printf("%s\n", $wordarray{$j});
  if ($durarray{$j} > $thr1)
    {
    #printf(OUT "word_dur %s %s %s %s %s %s * %s %s %s %s %s %s %s\n", $wordarray{$j-6}, $wordarray{$j-5}, $wordarray{$j-4}, $wordarray{$j-3}, $wordarray{$j-2}, $wordarray{$j-1}, $wordarray{$j}, $wordarray{$j+1}, $wordarray{$j+2}, $wordarray{$j+3}, $wordarray{$j+4}, $wordarray{$j+5}, $wordarray{$j+6});
    }
  $wordgap = $onsetarray{$j} - $onsetarray{$j-1} - $durarray{$j-1};
  if ($thr2 < $wordgap)
    {
    #printf(OUT "word_gap %f %s %s %s %s %s %s * %s %s %s %s %s %s %s\n", $wordgap, $wordarray{$j-6}, $wordarray{$j-5}, $wordarray{$j-4}, $wordarray{$j-3}, $wordarray{$j-2}, $wordarray{$j-1}, $wordarray{$j}, $wordarray{$j+1}, $wordarray{$j+2}, $wordarray{$j+3}, $wordarray{$j+4}, $wordarray{$j+5}, $wordarray{$j+6})

    printf(OUT "%s ...\n", $current_sentence);
    $wordgap_rounded = int($wordgap * 100 + 0.5)/100;
    $current_sentence = $wordgap_rounded . " " . $wordarray{$j};
    }
  else
    { $current_sentence = $current_sentence . " " . $wordarray{$j}; }
  }

close(OUT)


