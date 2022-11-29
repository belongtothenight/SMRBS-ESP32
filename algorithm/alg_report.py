import datetime


def init_sumfile(samp_dp, samp_ds, chunk, alpha, fp, fn):
    lines = [
        '>> Experiment detail:',
        '1. Put the speaker at the relatively same location as the different microphones to see whether all microphones have the same gain.'
        '2. .',
        '',
        '>> Experiment setup:',
        'source: smartphone --bluetooth--> speaker',
        'volume: max * 1 https://noises.online/',
        'signal_type: white noise',
        'signal_frequency_hz: N/A',
        'sampling_rate_hz: 16000',
        'distance_cm: 10',
        'height_cm: -3 (on table)',
        'run: 1',
        '',
        '>> Parameter',
        'samp_dp = {0}'.format(samp_dp),
        'samp_ds = {0}'.format(samp_ds),
        'chunk =   {0}'.format(chunk),
        'alpha =   {0}'.format(alpha),
        '',
        '>> Figure:',
        'content: power estimation result of each individual channel',
        'x-axis: samples',
        'y-axis: Watt',
        'title: the channel facing the audio source',
        'legend: final power estimation value of each channel',
        '',
        '>> Result: ({0})\n'.format(now),
    ]
    now = datetime.datetime.now()
    now = now.strftime("%Y/%m/%d:%H:%M:%S")
    # with open(fp + fn, 'w', encoding='utf-8') as f:
    # f.write('>> Experiment detail:\n')
    # f.write('Put the speaker at the relatively same location as the different microphones to see whether all microphones have the same gain.\n')
    # f.write('\n')
    # f.write('>> Experiment setup:\n')
    # f.write('source: smartphone --bluetooth--> speaker\n')
    # f.write('volume: max * 1 https://noises.online/\n')
    # f.write('signal_type: white noise\n')
    # f.write('signal_frequency_hz: N/A\n')
    # f.write('sampling_rate_hz: 16000\n')
    # f.write('distance_cm: 10\n')
    # f.write('height_cm: -3 (on table)\n')
    # f.write('run: 1\n')
    # f.write('\n')
    # f.write('>> Parameter\n')
    # f.write('samp_dp = {0}\n'.format(samp_dp))
    # f.write('samp_ds = {0}\n'.format(samp_ds))
    # f.write('chunk =   {0}\n'.format(chunk))
    # f.write('alpha =   {0}\n'.format(alpha))
    # f.write('\n')
    # f.write('>> Figure:\n')
    # f.write('content: power estimation result of each individual channel\n')
    # f.write('x-axis: samples\n')
    # f.write('y-axis: Watt\n')
    # f.write('title: the channel facing the audio source\n')
    # f.write('legend: final power estimation value of each channel\n')
    # f.write('\n')
    # f.write('>> Result: ({0})\n'.format(now))
    with open(fp + fn, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
