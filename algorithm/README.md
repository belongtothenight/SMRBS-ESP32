# Summary of algorithm

## 1. Function Structure

### 1.1 alg_test1.py ~ alg_test5.py

Not recorded.

### 1.2 [alg_test6.py](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_test6.py)

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

### 1.3 [alg_test7.py](https://github.com/belongtothenight/SMRBS-ESP32/blob/main/algorithm/alg_test7.py)

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
    - PE.cal_st()
    - *PE.store_data()
  - PE core/plot data
    - PE.plt_s()
    - PE.plt_p()
    - PE.plt_pe1()
    - PE.plt_cb11()
    - PE.plt_cb12()
- *PE extension
  - *PE.param_test()

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
