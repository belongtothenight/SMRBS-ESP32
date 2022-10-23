# Summary of algorithm

"alg_test" files are coded to create custome module for this project/repo.
"alg" file are the finished module integrated from generations of "alg_test" files.
Other files are used to do different measurements and experiments based on "alg" module.

## 1. ALG Function Structure

### 1.1 alg_test1.py ~ alg_test5.py

Not recorded.

### 1.2 [alg_test6.py](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test6.py)

- PE core
  - PE core/setup
    - PE.\_\_init__()
    - PE.terminate()
  - PE core/gather data
    - PE.read_6ch_data()
    - PE.pow()
  - PE core/algorithm
    - PE.pe1()
  - PE core/process data
    - PE.dc1()
    - PE.cal_st()
  - PE core/plot data
    - PE.plt_s()
    - PE.plt_p()
    - PE.plt_pe1()
    - PE.plt_cb11()
    - PE.plt_cb12()

### 1.3 [alg_test7.py](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test7.py)

- PE core
  - PE core/setup
    - PE.\_\_init__()
    - PE.terminate()
  - PE core/gather data
    - *PE.read_data()
    - PE.pow()
  - PE core/algorithm
    - PE.pe1()
  - PE core/process data
    - PE.dc1()
    - *PE.store_data()
    - *PE.evaluate()
  - PE core/plot data
    - PE.plt_s()
    - PE.plt_p()
    - PE.plt_pe1()
    - PE.plt_cb11()
    - PE.plt_cb12()
- *PE extension
  - *PE.continuous_run()
  - *PE.param_test()

### 1.4 [alg_test8.py](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_tests/alg_test8.py)

- PE core
  - PE core/setup
    - PE.\_\_init__()
    - PE.terminate()
  - PE core/gather data
    - PE.read_data()
    - PE.pow()
  - PE core/algorithm
    - PE.pe1()
  - PE core/process data
    - PE.dc1()
    - PE.store_data()
    - *PE.clear_data()
    - PE.evaluate()
  - PE core/plot data
    - PE.plt_s()
    - PE.plt_p()
    - PE.plt_pe1()
    - PE.plt_cb11()
    - PE.plt_cb12()
    - *PE.plt_cb13()
- PE extension
  - PE.continuous_run()
  - PE.param_test()

### 1.5 [alg.py](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg.py) (v1.0.2)

Full functionality of algorithm module.
Subfunctionns are tested and integrated to this file.

- PE core
  - PE core/setup
    - PE.\_\_init__()
    - PE.terminate()
  - PE core/gather data
    - PE.read_data()
    - PE.pow()
  - PE core/algorithm
    - PE.pe1()
  - PE core/process data
    - PE.dc1()
    - PE.store_data()
    - PE.evaluate()
  - PE core/plot data
    - PE.plt_s()
    - PE.plt_p()
    - PE.plt_pe1()
    - PE.plt_cb11()
    - PE.plt_cb12()
- PE extension
  - PE.continuous_run()
  - PE.param_test1()
  - PE.param_test2()

## 2. Change Log

| No. | File                        | Detail                                                      |
| :-: | --------------------------- | ----------------------------------------------------------- |
|  1  | alg_test1.py                | Add device testing code.                                    |
|  2  | alg_test2.py                | Add 4 channel data process.                                 |
|  3  | alg_test2.py                | Add 4 channel signal plot.                                  |
|  4  | alg_test3.py                | Add 4 channel power estimation calculation.                 |
|  5  | alg_test4.py                | Add 4 cnannel power estimation plot.                        |
|  6  | alg_test4.py                | Add LED (ring_pixel) indicating which direction is decided. |
|  7  | alg_test4.py                | Try threading plotting, but failed.                         |
|  8  | alg_test4.py                | Add auto skip if the program raise error(overflow).         |
|  9  | alg_test5_alpha.py          | Add parameter "alpha" testing ability.                      |
| 10  | alg_test5_chunk.py          | Add parameter "chunk" testing ability.                      |
| 11  | alg_test5_sampledownsize.py | Add parameter "sampledownsize" testing ability.             |
| 12  | alg_test6.py                | Rewrite into module.                                        |
| 13  | alg_test6.py                | Fix power estimation bug.                                   |
| 14  | alg_test6.py                | Add axis labels to plots.                                   |
| 15  | alg_test6.py                | Expand to 6 channel processing.                             |
| 16  | alg_test7.py                | Add parameter testing ability.                              |
| 17  | alg_test7.py                | Add pixel_ring control.                                     |
| 18  | alg_test7.py                | Remove unused channels.                                     |
| 19  | alg_test7.py                | Separate plotting with recording.                           |
| 20  | alg_test7.py                | Add continuous running mode.                                |
| 21  | alg_test7.py                | Add parameter testing mode.                                 |
| 22  | alg_test8.py                | Rewrite parameter testing mode.                             |
| 23  | alg.py                      | Combined functional subfunctions.                           |
| 24  | alg.py                      | Add parameter to customize img export directory.            |
