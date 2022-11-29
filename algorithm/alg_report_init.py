import datetime


def init_sumfile(samp_dp, samp_ds, chunk, alpha, fp, fn):
    now = datetime.datetime.now()
    now = now.strftime("%Y/%m/%d:%H:%M:%S")
    lines = [
        '>> Experiment detail:',
        '1. Put the speaker at the relatively same location as the different microphones to see whether all microphones have the same gain.',
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
        '>> Result: ({0})'.format(now),
    ]
    with open(fp + fn, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
