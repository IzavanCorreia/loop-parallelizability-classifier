# Changes to the real-world samples

Only evident defects that prevented a sample from compiling or running were fixed, with minimal changes. Five fixes correct a syntax error or an invalid character; Undefined #5 initializes a list that was indexed before being filled; Undefined #46 adds the usual escape test to the inner loop of a Mandelbrot computation, whose values otherwise overflowed. Afterwards, the samples on which the researchers' label and the dependence oracle disagreed were adjudicated (see the last section).

## Parallelizable #7: parameter declared as a literal (syntax error)

Before:
```python
def simular_temperaturas(50):
```
After:
```python
def simular_temperaturas(n=50):
```

## Parallelizable #159: extra closing parenthesis (syntax error)

Before:
```python
resultados.append((p, p[-3:])))
```
After:
```python
resultados.append((p, p[-3:]))
```

## Undefined #5: indexing an empty list in the first iteration (IndexError)

Before:
```python
prev_row = []
```
After:
```python
prev_row = [0] * size
```

## Undefined #40: identifier with a corrupted accent (invalid character)

Before:
```python
sa��da
```
After:
```python
saida
```

## Undefined #46: divergent points overflow the complex power (OverflowError); standard escape test added to the inner loop

Before:
```python
                z = z**2 + c
```
After:
```python
                z = z**2 + c
                if abs(z) > 2:
                    break
```

## Undefined #99: unbalanced bracket (syntax error)

Before:
```python
caracteres[(ord(senha[-1]) % len(caracteres)]
```
After:
```python
caracteres[ord(senha[-1]) % len(caracteres)]
```

## Undefined #110: unbalanced bracket (syntax error)

Before:
```python
caracteres[(ord(senha[-1]) % len(caracteres)]
```
After:
```python
caracteres[ord(senha[-1]) % len(caracteres)]
```

## Kept without changes

- Parallelizable #48: creates temporary files; kept as is, not executed by the oracle
- Undefined #30: recursion without a loop statement; kept as is, not analysable by the oracle
- Undefined #32: recursion without a loop statement; kept as is, not analysable by the oracle

- 3 groups of exact duplicates kept; they share the `group` id in `metadata.csv`.

## Adjudicated labels

The researchers' labels were compared with the dynamic dependence oracle (agreement 97.6%, Cohen's kappa 0.953 on the 337 samples the oracle can analyse). The disagreements were adjudicated in favour of the definition used in this study; for nested loops the label refers to the outermost loop.

- original Parallelizable #24 -> Undefined
- original Undefined #16 -> Parallelizable
- original Undefined #18 -> Parallelizable
- original Undefined #46 -> Parallelizable
- original Undefined #108 -> Parallelizable
- original Undefined #143 -> Parallelizable
- original Undefined #145 -> Parallelizable
- original Undefined #157 -> Parallelizable
