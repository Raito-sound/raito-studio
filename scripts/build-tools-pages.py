#!/usr/bin/env python3
"""Render the bilingual, static tool directory, introductions and practical guides."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://raito.studio'
DATE = '2026-09-07'

APPS = {
    'tally': {
        'category': 'UtilitiesApplication',
        'en': {
            'title': 'TALLY — Japanese Text Editor & Mora Counter',
            'lead': 'Write Japanese text. Count characters and the sounds in your lyrics.',
            'description': 'A free browser text editor for Japanese writing, character counts and kana-based mora analysis. Check lyrics line by line and export TXT files.',
            'summary': 'Keep your draft and its analysis together. TALLY helps you fit text to a character limit or compare the length of lyric lines, without uploading your writing.',
            'features': [('Character counts and targets', 'See total counts and counts excluding spaces or line breaks. Set a target and follow your progress.'), ('Line-by-line mora counts', 'Lyrics mode counts the kana-based rhythmic units of each line. Small ゃ・ゅ・ょ combine with the preceding kana; small vowels have a separate counting option.'), ('Writing modes', 'Choose Japanese prose, lyrics, social posts, YouTube descriptions or general writing. Readability indicators include average sentence length and kanji ratio.'), ('Drafts and revisions', 'Compare counts with a snapshot, keep text in three temporary slots and export a TXT file.')],
            'steps': ['Open TALLY and type, paste or import a text file with OPEN.', 'Choose Lyrics mode to see mora counts. For a lyric written in kanji, enter its intended reading in kana when checking the sound count.', 'Edit while comparing line lengths. Export important drafts with SAVE .txt.'],
            'limits': 'Mora analysis does not automatically convert kanji to readings and ignores non-kana text apart from supported long-sound marks. A mora count is a writing aid, not a count of musical beats or notes. Browser storage is local to this browser and can be cleared; export a backup.',
            'facts': [('Price', 'Free'), ('Processing', 'On your device'), ('Export', 'TXT')],
            'guide': 'japanese-lyrics-mora',
        },
        'ja': {
            'title': 'TALLY｜歌詞の音数・モーラ数と文字数を数えるブラウザエディタ',
            'lead': '文章の文字数と、歌詞の音数を確かめる。',
            'description': '日本語の文字数カウント、歌詞の行別モーラ数、文章分析に使える無料ブラウザエディタ。入力しながら確認でき、TXTで保存できます。',
            'summary': '原稿と分析結果を同じ画面で確認できるTALLY。文字数指定のある文章や、フレーズごとの長さをそろえたい歌詞を、書きながら調整できます。',
            'features': [('文字数と目標を確認', '総文字数、空白や改行を除いた文字数を表示。目標文字数を設定して進み具合を確認できます。'), ('歌詞を行ごとのモーラ数で比較', '作詞モードでは、かなをもとに各行のモーラ数を表示します。「ゃ・ゅ・ょ」は前のかなとまとめ、小書き母音は数え方を切り替えられます。'), ('用途別の分析', '日本語原稿、作詞、SNS、YouTube概要欄、汎用のモードを選択。平均文長や漢字率なども確認できます。'), ('推敲と保存', 'スナップショットで文字数の変化を比較。3つの一時保存スロットを使い、完成した文章はTXTで書き出せます。')],
            'steps': ['TALLYを開き、文章を入力・貼り付けするか、OPENからテキストファイルを読み込みます。', '作詞モードを選ぶと行別のモーラ数が表示されます。漢字を含む歌詞の音数を調べるときは、意図した読みをかなで入力します。', '行の長さを見ながら推敲し、SAVE .txtで大事な原稿を保存します。'],
            'limits': '漢字の読みは自動変換しません。モーラ計算では、対応する長音記号を除き、かな以外の文字を数えません。また、モーラ数と曲の拍数・音符数は同じではありません。一時保存は端末・ブラウザごとの保存なので、大切な原稿はファイルでも残してください。',
            'facts': [('料金', '無料'), ('文字の処理', '端末内'), ('書き出し', 'TXT')],
            'guide': 'japanese-lyrics-mora',
        },
    },
    'carve': {
        'category': 'MultimediaApplication',
        'en': {
            'title': 'CARVE — Browser Audio Editor for Trimming & Loop Editing',
            'lead': 'Trim audio, shape fades and listen closely to your loop seams.',
            'description': 'Edit audio in your browser for free. Trim selections, adjust fades and gain, check loop seams, and export WAV, OGG Vorbis or MP3 with CARVE.',
            'summary': 'Open an audio file and edit its waveform on your own device. CARVE combines everyday range editing with loop checks and sample-based OGG loop markers for game audio.',
            'features': [('Edit a range', 'Delete, copy, insert-paste or extract a selection. Selection edges can snap to nearby zero crossings; Shift-drag selects raw positions.'), ('Fades and levels', 'Choose from five fade curves, normalize to a target peak or adjust gain by a specified number of decibels.'), ('Check the join', 'Seam auditions the transition from the selection end back to its start. Markers let you define reusable loop boundaries.'), ('Export audio and loop tags', 'Export WAV at 16-bit, 24-bit or 32-bit float, OGG Vorbis or MP3. OGG exports include LOOPSTART and LOOPLENGTH when at least two markers are set.')],
            'steps': ['Open CARVE and drop an audio file into the editor, or use Open.', 'Select a range, adjust its fades or levels, and use Seam to hear the end-to-start transition.', 'For an OGG loop, set markers at the start and end. Choose your output format and use Export.'],
            'limits': 'Audio is processed locally. OGG and MP3 encoders are downloaded when needed, so those exports require a network connection. Input support depends on browser decoding. Use a desktop or laptop for precise waveform edits. A receiving player must support the OGG loop tags to use them.',
            'facts': [('Price', 'Free'), ('Processing', 'On your device'), ('Export', 'WAV / OGG / MP3')],
            'guide': 'audio-loop-seams',
        },
        'ja': {
            'title': 'CARVE｜ブラウザで音声カット・ループ編集できる無料ツール',
            'lead': '音声を切り出し、フェードを整え、ループの継ぎ目を聴く。',
            'description': 'インストール不要の無料音声編集ツール。ブラウザでトリミング、フェード、音量調整、ループ確認ができ、WAV・OGG・MP3に書き出せます。',
            'summary': '音声ファイルを開き、端末内で波形を編集するCARVE。短い素材の切り出しから、ゲーム音楽のループ確認、サンプル単位のOGGループタグまで扱えます。',
            'features': [('選択範囲を編集', '削除、コピー、挿入貼り付け、別ファイルへの切り出しに対応。選択端を近くのゼロクロスへ合わせられ、Shiftを押しながらドラッグすると補正なしで選択できます。'), ('フェードと音量を調整', '5種類のフェードカーブ、指定ピークへのノーマライズ、dB単位のゲイン調整を使えます。'), ('継ぎ目を短時間で確認', 'Seamで選択範囲の終端から先頭へのつながりを試聴。マーカーでループの開始点と終了点を指定できます。'), ('形式を選んで書き出し', 'WAVは16bit・24bit・32bit floatに対応。OGGとMP3にも書き出せます。2つ以上のマーカーがあるOGG出力にはLOOPSTART・LOOPLENGTHを記録します。')],
            'steps': ['CARVEを開き、音声ファイルをドロップするか、Openで読み込みます。', '範囲を選択してフェードや音量を調整し、Seamで終端から先頭へのつながりを確認します。', 'OGGループを書き出す場合は開始・終了のマーカーを設定。出力形式を選び、Exportで保存します。'],
            'limits': '音声は端末内で処理します。OGG・MP3は必要に応じてエンコーダーを取得するため、書き出しにネット接続が必要です。読み込み形式はブラウザのデコード対応に依存します。細かな波形編集にはPCを推奨。ループタグを利用するには再生側の対応も必要です。',
            'facts': [('料金', '無料'), ('音声の処理', '端末内'), ('書き出し', 'WAV / OGG / MP3')],
            'guide': 'audio-loop-seams',
        },
    },
    'keys': {
        'category': 'MultimediaApplication',
        'en': {
            'title': 'KEYS — Online Piano & Organ with Recording and WAV Export',
            'lead': 'Play a phrase. Practice it. Keep the idea.',
            'description': 'A free browser piano and organ with a metronome and phrase recording. Play with your computer keyboard or touch, then export MIDI or WAV.',
            'summary': 'KEYS is a browser keyboard for trying melodies, practicing with a metronome and keeping short musical ideas. Choose a sampled piano or an organ sound and start playing.',
            'features': [('Piano and organ', 'Switch between a sampled grand piano and synthesized organ. Adjust volume, tone and room effect.'), ('Keyboard and touch', 'Play with computer keys, mouse or touch. Change octave and transpose, and use sustain. Touch users can scroll the keyboard to reach more notes.'), ('Practice tools', 'Set the metronome from 30 to 240 BPM with beat and subdivision options. See sounding notes and practical chord labels.'), ('Record and export', 'Capture takes up to 90 seconds, use count-in or looped playback, and export MIDI or stereo 44.1 kHz / 16-bit PCM WAV. The metronome is not included in exports.')],
            'steps': ['Open KEYS and select Enable audio. Use an English keyboard input source for the displayed key bindings.', 'Choose piano or organ, set a comfortable level and play with the on-screen keyboard or computer keys.', 'Open the recorder, capture a short take, then export MIDI or WAV to keep it.'],
            'limits': 'A new completed take replaces the previous take. Export files to keep multiple ideas. Computer keyboards do not measure playing velocity and may limit simultaneous keys. MIDI controller input is not implemented. Chord labels cover common exact note combinations, not complete harmonic analysis.',
            'facts': [('Price', 'Free'), ('Sounds', 'Piano / Organ'), ('Export', 'MIDI / WAV')],
        },
        'ja': {
            'title': 'KEYS｜録音・WAV保存できる無料ブラウザピアノとオルガン',
            'lead': '浮かんだフレーズを弾いて、練習して、残す。',
            'description': 'PCのキーボードやタッチで弾ける無料オンラインピアノ・オルガン。メトロノーム、短い演奏の録音、MIDI・WAV保存に対応しています。',
            'summary': 'メロディーを試し、メトロノームに合わせて練習し、短いアイデアを残すブラウザ鍵盤。サンプル音源のピアノと、合成音源のオルガンを選べます。',
            'features': [('ピアノとオルガン', 'グランドピアノのサンプル音とオルガンを切り替え、音量・音色・残響を調整できます。'), ('PCキーとタッチで演奏', 'PCのキー、マウス、タッチで演奏。オクターブ移動、移調、サステインに対応し、タッチでは鍵盤を横にスクロールできます。'), ('練習の補助', '30〜240 BPMのメトロノームに拍数・細分化の設定を搭載。鳴っている音名と代表的なコード名を表示します。'), ('録音して持ち出す', '最大90秒のテイクを録音し、カウントインやループ再生を使えます。MIDIとステレオ44.1kHz・16bit PCM WAVに書き出し可能。メトロノームは出力音声に含めません。')],
            'steps': ['KEYSを開いてEnable audioを押します。PCキーで弾く場合は英語入力に切り替えます。', 'ピアノかオルガンを選び、音量を調整して画面の鍵盤やPCキーで演奏します。', 'レコーダーを開いて短いテイクを録音し、MIDIまたはWAVで保存します。'],
            'limits': '新しく録音したテイクは前のテイクを置き換えます。複数のアイデアはファイルに書き出して残してください。PCキーボードは打鍵の強さを検出せず、同時押し数にも機器ごとの制限があります。MIDI鍵盤入力は未対応。コード表示は代表的な音の組み合わせを示す補助機能です。',
            'facts': [('料金', '無料'), ('音色', 'ピアノ / オルガン'), ('書き出し', 'MIDI / WAV')],
        },
    },
    'pitch': {
        'category': 'MultimediaApplication',
        'en': {
            'title': 'PITCH — Free Online Guitar & Bass Tuner',
            'lead': 'A clear meter for tuning guitar, bass and more.',
            'description': 'Tune guitar, bass, ukulele and strings in your browser. PITCH offers a large cents meter, tuning presets, a visual strobe and reference tones for free.',
            'summary': 'PITCH puts the detected note and tuning error at the center of the screen. Use automatic string selection, lock a string or switch to chromatic tuning for other instruments.',
            'features': [('A meter you can read', 'See note, frequency and cents deviation with needle or visual strobe modes. Select a ±50, ±25 or ±10 cent range and expand the meter for focus.'), ('Instrument presets', 'Choose guitar, bass, ukulele, bowed strings or banjo presets, including alternate guitar tunings. Chromatic mode and custom tunings cover other setups.'), ('Adjust your reference', 'Set A4 between 400 and 480 Hz, capo offset and the in-tune tolerance. Play reference tones when you want to compare by ear.'), ('Input and history', 'Choose an available audio input, adjust smoothing and noise gate, and view recent pitch history. Compact controls adapt to phone screens.')],
            'steps': ['Open PITCH, choose your instrument and tuning, and check the A4 reference.', 'Select Start microphone and allow microphone access. Play one string at a time with the other strings muted.', 'Follow the note and cents meter. Adjust the string toward the center, then stop the microphone when finished.'],
            'limits': 'Microphone permission is required for detection. Input audio is processed on your device and is not uploaded. Quiet surroundings and a clear single note help; chords, noise and harmonics can make readings unstable. Device microphones and browsers affect results. Reference tones use the speakers, so stop them before measuring if they feed back into the microphone.',
            'facts': [('Price', 'Free'), ('Input', 'Microphone / audio input'), ('Audio processing', 'On your device')],
        },
        'ja': {
            'title': 'PITCH｜ギター・ベース対応の無料オンラインチューナー',
            'lead': 'ギターもベースも、見やすいメーターで合わせる。',
            'description': 'ブラウザで使える無料ギター・ベースチューナー。大きなセントメーター、変則チューニング、ウクレレ・弦楽器、基準音とストロボ表示に対応。',
            'summary': '音名と音程のずれを画面の中心で確認できるPITCH。弦の自動選択や固定、クロマチックモードを使って、楽器に合わせてチューニングできます。',
            'features': [('音程のずれを大きく表示', '音名、周波数、セントのずれを確認。針とビジュアルストロボの表示を選べ、±50・±25・±10セントに切り替えたり、メーターを拡大したりできます。'), ('楽器と変則チューニング', 'ギター、ベース、ウクレレ、弓奏弦楽器、バンジョーなどのプリセットを搭載。クロマチックとカスタム設定も使えます。'), ('基準音を調整', 'A4を400〜480Hzで設定し、カポ補正や合格範囲も調整。基準音を鳴らして耳で合わせることもできます。'), ('入力と履歴', '利用できる音声入力を選び、表示の平滑化やノイズゲートを調整。直近の音程履歴を確認でき、スマートフォンでは補助パネルを開閉できます。')],
            'steps': ['PITCHを開き、楽器とチューニングを選んでA4の基準を確認します。', 'Start microphoneを押し、マイクの使用を許可します。他の弦をミュートして、1本ずつ鳴らしてください。', '音名とセントの表示を見ながら中央に合わせ、終わったらマイクを停止します。'],
            'limits': '音程の検出にはマイク使用の許可が必要です。入力音声は端末内で処理し、アップロードしません。和音、周囲の雑音、強い倍音は表示が安定しない原因になります。端末のマイクやブラウザによっても結果は変わります。基準音がマイクに回り込む場合は、基準音を止めてから測定してください。',
            'facts': [('料金', '無料'), ('入力', 'マイク / 音声入力'), ('音声の処理', '端末内')],
        },
    },
}

GUIDES = {
    'japanese-lyrics-mora': {
        'app': 'tally',
        'en': {
            'title': 'Count the Sounds in Japanese Lyrics: Characters vs Mora',
            'description': 'Learn why character counts and mora counts differ, then check a short Japanese lyric line by line in TALLY. Includes kana examples and counting limitations.',
            'intro': 'A lyric can have the same number of written characters as another line and still feel longer when sung. Count the intended pronunciation first, then sing it against the melody. TALLY helps with the first check.',
            'body': '''<h2>Start with the reading, not the kanji</h2><p>The word 今日 has two written characters. Its reading きょう has three kana characters, but two mora: きょ・う. Small ゃ, ゅ and ょ combine with the preceding kana. The sounds っ, ん and the long-vowel mark ー each contribute a mora in these examples.</p><div class="table-scroll"><table><caption>Kana examples with TALLY's small-vowel option off</caption><thead><tr><th scope="col">Text</th><th scope="col">Characters</th><th scope="col">Mora</th><th scope="col">Breakdown</th></tr></thead><tbody><tr><td lang="ja">きょう</td><td>3</td><td>2</td><td lang="ja">きょ・う</td></tr><tr><td lang="ja">がっこう</td><td>4</td><td>4</td><td lang="ja">が・っ・こ・う</td></tr><tr><td lang="ja">しんぶん</td><td>4</td><td>4</td><td lang="ja">し・ん・ぶ・ん</td></tr><tr><td lang="ja">キャット</td><td>4</td><td>3</td><td lang="ja">キャ・ッ・ト</td></tr><tr><td lang="ja">コーヒー</td><td>4</td><td>4</td><td lang="ja">コ・ー・ヒ・ー</td></tr></tbody></table></div><h2>Try a short phrase in TALLY</h2><p>Paste this original practice text into the editor, switch to Lyrics mode, and show the line-end mora counts:</p><pre lang="ja">きょうも\nそらを\nみあげる</pre><p>The lines contain <strong>3, 3 and 4 mora</strong>, for a total of 10. They contain 4, 3 and 4 written kana characters; the difference is the small ょ in the first line. Keep each melodic phrase on its own line to compare lengths.</p><p>Now replace きょうも with あしたも. The first line becomes four mora. Whether that fits is a musical decision: sing both versions at the intended tempo and check where the consonants and vowel changes fall.</p><h2>Use the count as a starting point</h2><p>Mora are not the same as musical beats, syllables in every language, or the number of notes. A vowel can stretch over several notes; a melody can also fit multiple sounds inside one beat. Matching counts alone does not guarantee natural phrasing or word stress.</p><h2>Know what the counter reads</h2><p>TALLY counts kana rather than converting kanji to pronunciation. Enter the intended reading yourself, especially for names or words with more than one reading. Non-kana text is ignored by mora analysis apart from supported long-sound marks. Use full-width kana for the examples here.</p><p>The small-vowel option changes how letters such as ァ and ぇ are counted. With it off, ファ counts as one mora; with it on, it counts as two. Choose a convention that matches your lyric draft and keep it consistent while comparing versions.</p><h2>Keep the sung version</h2><p>After checking the count, return to the spelling you want to deliver, sing the phrase, and export a TXT copy. Browser storage is convenient for drafting, but it should not be your only copy of finished lyrics.</p>''',
        },
        'ja': {
            'title': '歌詞の音数を数えるには？文字数とモーラ数の違い',
            'description': '「きょう」は3文字でも2モーラ。歌詞の音数と文字数の違いを、かなの具体例とTALLYの操作で解説します。漢字や小書き文字の注意点も紹介。',
            'intro': '文字数が同じ歌詞でも、歌うと長さが違って感じられることがあります。まず意図した読みの音数を確認し、そのあとメロディーに乗せて歌ってみる。TALLYは、その最初の確認を助けるツールです。',
            'body': '''<h2>漢字の字数ではなく、読みから数える</h2><p>「今日」は漢字では2文字、読みの「きょう」はかなで3文字です。一方、モーラで区切ると「きょ・う」の2つになります。小さい「ゃ・ゅ・ょ」は前のかなとまとまり、次の例では「っ」「ん」「ー」はそれぞれ1モーラとして数えます。</p><div class="table-scroll"><table><caption>TALLYで小書き母音の分割をオフにした場合の例</caption><thead><tr><th scope="col">表記</th><th scope="col">文字数</th><th scope="col">モーラ数</th><th scope="col">区切り</th></tr></thead><tbody><tr><td>きょう</td><td>3</td><td>2</td><td>きょ・う</td></tr><tr><td>がっこう</td><td>4</td><td>4</td><td>が・っ・こ・う</td></tr><tr><td>しんぶん</td><td>4</td><td>4</td><td>し・ん・ぶ・ん</td></tr><tr><td>キャット</td><td>4</td><td>3</td><td>キャ・ッ・ト</td></tr><tr><td>コーヒー</td><td>4</td><td>4</td><td>コ・ー・ヒ・ー</td></tr></tbody></table></div><h2>短い練習文をTALLYに入れる</h2><p>次の練習用の文をエディタに貼り付け、作詞モードに切り替えて「行末モーラ」を表示します。</p><pre>きょうも\nそらを\nみあげる</pre><p>各行のモーラ数は<strong>3・3・4、合計10</strong>です。かなの文字数は4・3・4。「きょうも」の小さい「ょ」が、文字数とモーラ数の差になっています。メロディーのひとまとまりごとに改行すると、行の長さを比較しやすくなります。</p><p>今度は「きょうも」を「あしたも」に変えてみてください。最初の行は4モーラになります。それが曲に合うかどうかは、実際のテンポで両方を歌い、子音や母音の変わる位置を確かめて判断します。</p><h2>モーラ数と音符の数は別に考える</h2><p>モーラは曲の拍数や音符数と同じものではありません。ひとつの母音を複数の音符に伸ばすことも、1拍の中に複数の音を収めることもあります。数がそろっていても、言葉のアクセントやフレーズの切れ方が自然に聞こえるとは限りません。</p><h2>漢字と小書き母音に注意する</h2><p>TALLYは、漢字を読みに変換してから数える仕組みではありません。人名や複数の読みがある語は特に、歌いたい読みを自分でかなにして入力してください。モーラ計算では、対応する長音記号を除き、かな以外を無視します。ここでの例は全角かなを使っています。</p><p>「小書ァを1拍」は「ァ」「ぇ」などの数え方を変える設定です。オフなら「ファ」は1モーラ、オンなら2モーラになります。比較中に条件が変わらないよう、原稿に合う数え方を決めて使ってください。</p><h2>最後は歌って、原稿を保存する</h2><p>確認が終わったら提出したい表記へ戻し、メロディーに合わせて歌ってみましょう。完成稿はTXTでも書き出します。ブラウザの一時保存だけに頼らず、歌詞のファイルを残しておくと安心です。</p>''',
        },
    },
    'audio-loop-seams': {
        'app': 'carve',
        'en': {
            'title': 'How to Check and Improve an Audio Loop Seam in CARVE',
            'description': 'Audition an audio loop join, adjust its boundaries and export OGG loop markers with CARVE. Includes a 48 kHz sample-position example and practical caveats.',
            'intro': 'A loop has to connect musically as well as at the waveform level. CARVE lets you hear the end-to-start transition directly, so you can check the join without listening through the entire file each time.',
            'body': '''<h2>Choose a musical boundary first</h2><p>Open an audio file that you have permission to edit. Find a start and end that belong together rhythmically and harmonically. A technically quiet cut can still feel wrong if it drops a beat, truncates a reverb tail or jumps to a different musical phrase.</p><h2>Select the loop and use Seam</h2><ol><li>Drag across the waveform to select the intended loop. Selection edges snap to nearby zero crossings; hold Shift while dragging for a raw position.</li><li>Press <strong>Seam</strong>. CARVE plays up to one second before the selection end and then continues from its start. With no selection, it checks the file end against the file start.</li><li>Listen for a click, sudden level change, missing beat or interrupted ambience. Adjust a boundary and audition again.</li></ol><h2>Zero crossings help, but listen to both channels</h2><p>A sudden jump in sample amplitude can cause a click. Crossing near zero can reduce that jump, but it does not guarantee a clean join: the waveform direction, stereo channels and surrounding sound may still differ. CARVE's zero-cross search uses the first channel, so listen to the complete stereo result.</p><p>If the waveform joins but the music still lurches, revisit the phrase boundary. A fade to silence at each end can be useful for a standalone sound, but on a repeating music loop it can create an audible dip. Do not treat a fade as an automatic seamless-loop fix.</p><h2>Set the two markers for OGG export</h2><p>Place the play cursor at the start and press M, then repeat at the end. Keep the intended loop boundaries as the first two markers in time order. The Snap control affects marker placement on the beat grid; use Shift when you need to bypass that grid. Double-click between the markers to select their span and run Seam again.</p><p>When you export OGG, CARVE writes <code>LOOPSTART</code> from the first marker and <code>LOOPLENGTH</code> from the distance between the first two. Selecting audio alone does not create these tags.</p><div class="table-scroll"><table><caption>Example: a loop from 2 seconds to 10 seconds at 48 kHz</caption><tbody><tr><th scope="row">Start</th><td>2 × 48,000 = 96,000 samples</td></tr><tr><th scope="row">End</th><td>10 × 48,000 = 480,000 samples</td></tr><tr><th scope="row">LOOPSTART</th><td>96000</td></tr><tr><th scope="row">LOOPLENGTH</th><td>480,000 − 96,000 = 384000</td></tr></tbody></table></div><h2>Check the exported file in its destination</h2><p>Loop tags are sample positions, not milliseconds. Resampling changes their meaning unless the positions are recalculated. OGG encoding needs a network connection to load the encoder, and the destination player or game engine must support the loop tags.</p><p>Reopen the exported OGG in CARVE to check the restored markers, then test it in the actual playback environment. That final check catches differences that an editor-only audition cannot establish.</p><p><a href="https://carve.raito.studio/manual.html#markers">CARVE manual: markers</a> · <a href="https://carve.raito.studio/manual.html">Full manual and loop-tag reference</a></p>''',
        },
        'ja': {
            'title': 'ループ音源の継ぎ目を自然にするには？CARVEで確認する手順',
            'description': 'ブラウザ音声編集ツールCARVEでループの継ぎ目を試聴し、開始・終了点を調整する方法。OGGループタグと48kHzのサンプル数の具体例も解説。',
            'intro': 'ループは、波形だけでなく音楽としても自然につながる必要があります。CARVEのSeamを使うと終端から先頭へのつながりだけを聴けるので、毎回ファイル全体を再生せずに調整できます。',
            'body': '''<h2>まず音楽としてつながる位置を探す</h2><p>編集する権利のある音声ファイルを開き、リズムや和声がつながる開始点と終了点を探します。波形上では静かな切れ目でも、拍が抜けたり、リバーブの余韻が途切れたり、別のフレーズへ飛んだりすると不自然に聞こえます。</p><h2>範囲を選んでSeamで聴く</h2><ol><li>波形をドラッグしてループさせたい範囲を選択します。選択端は近くのゼロクロスへ補正されます。補正なしで指定したいときはShiftを押しながらドラッグします。</li><li><strong>Seam</strong>を押します。選択範囲の終端直前を最大1秒再生し、そのまま先頭へつなげて試聴します。範囲が未選択ならファイル全体の終端と先頭を確認します。</li><li>クリック音、急な音量変化、拍の欠落、響きの途切れを聴き取り、境界を動かしてもう一度確認します。</li></ol><h2>ゼロクロスだけで判断しない</h2><p>サンプルの振幅が境界で急に飛ぶと、クリック音の原因になります。ゼロ付近でつなぐと差を小さくできる場合がありますが、波形の進む方向やステレオの左右、前後の音色まで一致するとは限りません。CARVEのゼロクロス探索は第1チャンネルを参照するため、ステレオ全体を耳でも確認してください。</p><p>波形はつながっているのに音楽がつまずく場合は、フレーズの境界を見直します。単発の効果音なら両端を無音へフェードする方法もありますが、音楽のループでは繰り返すたびに音量が落ちることがあります。フェードをかければ必ず解決するわけではありません。</p><h2>OGG出力には開始・終了のマーカーを置く</h2><p>開始点に再生カーソルを置いてMを押し、終了点にも同様にマーカーを置きます。時間順で最初の2つが意図したループの境界になるようにしてください。Snapはマーカーを拍グリッドへ合わせる設定です。グリッドに合わせたくない場合はShiftを使います。マーカー間をダブルクリックして範囲選択し、Seamで再確認します。</p><p>OGGを書き出すと、最初のマーカーが<code>LOOPSTART</code>、最初の2つのマーカーの距離が<code>LOOPLENGTH</code>に入ります。音声の範囲を選択しただけでは、このタグは作られません。</p><div class="table-scroll"><table><caption>48kHzの音源で、2秒から10秒までをループする例</caption><tbody><tr><th scope="row">開始点</th><td>2 × 48,000 = 96,000サンプル</td></tr><tr><th scope="row">終了点</th><td>10 × 48,000 = 480,000サンプル</td></tr><tr><th scope="row">LOOPSTART</th><td>96000</td></tr><tr><th scope="row">LOOPLENGTH</th><td>480,000 − 96,000 = 384000</td></tr></tbody></table></div><h2>最後は書き出したファイルを再生先で確認する</h2><p>ループタグの単位はミリ秒ではなくサンプルです。サンプルレートを変換すると、位置を計算し直さない限り指定先が変わります。OGG出力にはエンコーダー取得のためネット接続が必要で、再生するプレイヤーやゲームエンジン側にもループタグ対応が必要です。</p><p>書き出したOGGをCARVEで開き直してマーカーを確認し、実際に使う再生環境でもループさせてください。編集画面だけでは分からない再生側の差を、最後に確認できます。</p><p><a href="https://carve.raito.studio/manual.html#markers">CARVEのマーカー操作マニュアル（英語）</a> · <a href="https://carve.raito.studio/manual.html">操作とループタグの全マニュアル（英語）</a></p>''',
        },
    },
}


def path_for(slug, lang):
    return f'/{"ja/" if lang == "ja" else ""}{slug}/'


def render(slug, lang, title, description, body, kind='WebPage', app=None):
    url = ORIGIN + path_for(slug, lang)
    en = ORIGIN + path_for(slug, 'en')
    ja = ORIGIN + path_for(slug, 'ja')
    is_ja = lang == 'ja'
    data = {'@context': 'https://schema.org', '@type': kind, 'url': url, 'name': title,
            'description': description, 'inLanguage': lang,
            'isPartOf': {'@id': ORIGIN + '/#website'}}
    if app:
        data['about'] = {'@type': 'WebApplication', '@id': f'https://{app}.raito.studio/#app',
                         'name': app.upper(), 'url': f'https://{app}.raito.studio/',
                         'applicationCategory': APPS[app]['category'], 'operatingSystem': 'Web browser',
                         'isAccessibleForFree': True, 'creator': {'@id': ORIGIN + '/#person'}}
    if kind == 'Article':
        data.update({'headline': title, 'datePublished': DATE, 'dateModified': DATE,
                     'author': {'@type': 'Organization', 'name': 'Raito Studio Tools', 'url': ORIGIN + '/tools/'}})
    en_current = ' aria-current="page"' if not is_ja else ''
    ja_current = ' aria-current="page"' if is_ja else ''
    lang_switch = f'<a href="{path_for(slug, "en")}" lang="en" hreflang="en"{en_current}>English</a><span aria-hidden="true">/</span><a href="{path_for(slug, "ja")}" lang="ja" hreflang="ja"{ja_current}>日本語</a>'
    tools_path = path_for('tools', lang)
    document_title = title if title.startswith('Raito Studio Tools') else title + ' | Raito Studio Tools'
    html = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(document_title)}</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{en}"><link rel="alternate" hreflang="ja" href="{ja}"><link rel="alternate" hreflang="x-default" href="{en}">
<meta name="robots" content="index,follow"><meta name="theme-color" content="#efede5">
<meta property="og:type" content="{'article' if kind == 'Article' else 'website'}"><meta property="og:site_name" content="Raito Studio Tools"><meta property="og:locale" content="{'ja_JP' if is_ja else 'en_US'}"><meta property="og:url" content="{url}"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/site.css?v=lang-20260911"><link rel="stylesheet" href="/apps.css?v=lang-20260911">
<script type="application/ld+json">{json.dumps(data, ensure_ascii=False).replace('<', '&lt;')}</script><script src="/lang.js" defer></script></head>
<body id="top" class="app-page {app or 'tools-hub'}"><a class="skip-link" href="#main">{'本文へ' if is_ja else 'Skip to content'}</a>
<header class="site-header"><a class="brand" href="/" aria-label="Raito.studio home"><img src="/assets/raito-logo.svg" alt="Raito / 来兎" width="84" height="44"></a><nav aria-label="{'メインナビゲーション' if is_ja else 'Primary navigation'}"><a href="/">Home</a><a href="/works/">Works</a><a href="{tools_path}" aria-current="{'page' if slug == 'tools' else 'false'}">Tools</a><a href="/press/?lang={'ja' if is_ja else 'en'}">Press</a></nav><div class="header-right"><nav class="lang-switch" aria-label="{'言語' if is_ja else 'Language'}"><a href="{path_for(slug, "en")}" lang="en" hreflang="en" data-lang-switch="en"{en_current}>EN</a><span aria-hidden="true">/</span><a href="{path_for(slug, "ja")}" lang="ja" hreflang="ja" data-lang-switch="ja"{ja_current}>日本語</a></nav><a class="header-contact" href="{'/ja/#contact' if is_ja else '/#contact'}">{'お問い合わせ' if is_ja else 'Contact'} ↗</a></div></header>
<main id="main" class="app-main"><div class="tools-topline"><nav class="app-breadcrumb" aria-label="Breadcrumb"><a href="/">Raito.studio</a><span aria-hidden="true">/</span><a href="{tools_path}">Tools</a></nav><nav class="language-links" aria-label="Language">{lang_switch}</nav></div>{body}</main>
<footer><span>© 2026 RAITO.STUDIO</span><a href="{tools_path}">{'ツール一覧' if is_ja else 'ALL TOOLS'}</a><a href="#top">{'ページ先頭へ' if is_ja else 'BACK TO TOP'} ↑</a></footer></body></html>'''
    destination = ROOT / path_for(slug, lang).strip('/') / 'index.html'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html + '\n')


def guide_cards(lang):
    return ''.join(f'<a class="guide-card" href="{path_for("guides/" + slug, lang)}"><span class="app-category">{g["app"].upper()} / GUIDE</span><h3>{escape(g[lang]["title"])}</h3><p>{escape(g[lang]["description"])}</p><span aria-hidden="true">↗</span></a>' for slug, g in GUIDES.items())


def build():
    for lang in ['en', 'ja']:
        ja = lang == 'ja'
        for slug, app in APPS.items():
            d = app[lang]
            facts = ''.join(f'<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in d['facts'])
            features = ''.join(f'<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in d['features'])
            steps = ''.join(f'<li>{escape(s)}</li>' for s in d['steps'])
            extra = ''
            if slug in ['tally', 'carve']:
                extra += f'<a class="app-secondary" href="https://github.com/Raito-sound/{slug}">{"ソースコード" if ja else "Source on GitHub"} ↗</a>'
            if slug == 'carve':
                extra += '<a class="app-secondary" href="https://carve.raito.studio/manual.html">Manual (English) ↗</a>'
            guide = ''
            if d.get('guide'):
                guide = f'<section class="guide-callout"><p class="app-category">PRACTICAL GUIDE</p><h2><a href="{path_for("guides/" + d["guide"], lang)}">{escape(GUIDES[d["guide"]][lang]["title"])}</a></h2></section>'
            related = ''.join(f'<a href="{path_for(other,lang)}">{other.upper()} — {escape(APPS[other][lang]["lead"])}</a>' for other in APPS if other != slug)
            body = f'''<section class="app-hero"><div><p class="app-category">RAITO STUDIO TOOLS / {slug.upper()}</p><h1>{slug.upper()}</h1><p class="app-lead">{escape(d['lead'])}</p></div><div class="app-summary"><p>{escape(d['summary'])}</p><div class="app-actions"><a class="app-open" href="https://{slug}.raito.studio/">{slug.upper() + 'を使う' if ja else 'Open ' + slug.upper()} <span aria-hidden="true">↗</span></a>{extra}</div></div></section>
<dl class="app-facts">{facts}</dl><section class="app-detail"><h2>{'できること' if ja else 'What you can do'}</h2><dl class="app-features">{features}</dl></section><section class="app-detail"><h2>{'使い始めるには' if ja else 'Get started'}</h2><ol class="app-steps">{steps}</ol></section><section class="app-detail"><h2>{'使う前に知っておくこと' if ja else 'Before you start'}</h2><p class="reading-copy">{escape(d['limits'])}</p></section>{guide}<aside class="tools-related"><h2>{'ほかのツール' if ja else 'More tools by Raito'}</h2>{related}</aside>'''
            render(slug, lang, d['title'], d['description'], body, app=slug)
        cards = ''.join(f'<article class="tool-card {slug}"><p class="app-category">{slug.upper()}</p><h2><a href="{path_for(slug,lang)}">{escape(app[lang]["lead"])}</a></h2><p>{escape(app[lang]["description"])}</p><div class="app-actions"><a href="{path_for(slug,lang)}">{"使い方・機能" if ja else "Features & how to use"} ↗</a><a href="https://{slug}.raito.studio/">{"アプリを開く" if ja else "Open app"} ↗</a></div></article>' for slug, app in APPS.items())
        title = 'Raito Studio Tools｜作詞・音声編集・鍵盤・チューニングの無料ツール' if ja else 'Raito Studio Tools — Free Browser Tools for Writing & Music'
        description = '作曲家・来兎の無料ブラウザツール。TALLYで歌詞の音数を確認、CARVEで音声編集、KEYSでピアノ演奏と録音、PITCHでギター・ベースのチューニング。' if ja else 'Free browser tools by composer Raito: TALLY for Japanese lyrics and text, CARVE for audio editing, KEYS for piano and recording, and PITCH for tuning instruments.'
        body = f'''<section class="tools-intro"><p class="app-category">RAITO STUDIO TOOLS</p><h1>{'言葉を書く。音を整える。' if ja else 'Tools for writing. Tools for music.'}</h1><p class="app-lead">{escape(description)}</p><p>{'インストール不要。文章や演奏・入力音声は、それぞれのツールで端末内処理します。' if ja else 'Open a tool in your browser. Your writing, performances and input audio are processed on your device.'}</p><a class="app-secondary" href="/#profile">{'作曲家・来兎について' if ja else 'About Raito, composer and sound designer'} ↗</a></section><section class="tools-grid" aria-label="{'4つのツール' if ja else 'Four browser tools'}">{cards}</section><section class="tools-guides"><p class="app-category">PRACTICAL GUIDES</p><h2>{'具体例から使ってみる' if ja else 'Put the tools to work'}</h2><div class="guide-grid">{guide_cards(lang)}</div></section>'''
        render('tools', lang, title, description, body, kind='CollectionPage')
        for slug, guide in GUIDES.items():
            d = guide[lang]
            app = guide['app']
            body = f'''<article class="guide-article"><header class="guide-heading"><p class="app-category">{app.upper()} / PRACTICAL GUIDE</p><h1>{escape(d['title'])}</h1><p class="guide-meta">Raito Studio Tools · <time datetime="{DATE}">{DATE}</time></p><p class="app-lead">{escape(d['intro'])}</p><div class="app-actions"><a class="app-open" href="https://{app}.raito.studio/">{app.upper() + 'を開いて試す' if ja else 'Try it in ' + app.upper()} ↗</a><a href="{path_for(app,lang)}">{app.upper() + 'の機能と使い方' if ja else app.upper() + ' features & quick start'}</a></div></header><div class="guide-body">{d['body']}</div></article><aside class="tools-guides"><h2>{'関連する解説' if ja else 'More practical guides'}</h2><div class="guide-grid">{guide_cards(lang)}</div></aside>'''
            render('guides/' + slug, lang, d['title'], d['description'], body, kind='Article', app=app)
    print('Rendered 14 bilingual tool, directory and guide pages.')


if __name__ == '__main__':
    build()
