# Bus Matrix

A bus matrix mostra como as tabelas de fatos e dimensões se relacionam.

Cada linha é uma tabela de fato, e cada coluna uma tabela de dimensão.

Em um modelo estrela, as tabelas aparecem exatamente uma vez na bus matrix, seja como linhas ou colunas. Já no modelo
snowflake, as tabelas podem aparecer mais de uma vez.


| Processo de negócio    | Tabela                               | 	Granularidade     | Medida | Calendário | V_PRPGP_TIPOS_COTAS | V_PRPGP_CONCURSOS | V_PRPGP_CURSOS_POS | V_PRPGP_DOCENTES_POS | V_PRPGP_DISCENTES_POS | V_PRPGP_DISCIPLINAS_POS | V_PRPGP_DEFESAS | V_PRPGP_MEMBROS_EXTERNOS_BANCAS | PM_PROJETOS_PARTICIPANTES | V_PRPGP_PROJETOS_POS_ORGAOS |   
|:-----------------------|:-------------------------------------|:-------------------|:-------|:-----------|:--------------------|:------------------|--------------------|----------------------|:----------------------|:------------------------|:----------------|---------------------------------|:--------------------------|:----------------------------|
| Atratividade de cursos | V_PRPGP_CONCURSOS                    | Concurso           |        | ✔️         | ✔️                  |                   |                    |                      |                       |                         |                 |                                 |                           |                             |
| Atratividade de cursos | V_PRPGP_VAGAS_INSCRITOS_MATRICULADOS | Concurso/Cota/Vaga |        |            |                     | ✔️                | ✔️                 |                      |                       |                         |                 |                                 |                           |                             |
| Turmas                 | V_PRPGP_TURMAS_POS                   | Turma              |        | ✔️         |                     |                   |                    | ✔️                   | ✔️                    | ✔️                      |                 |                                 |                           |                             |
| Bancas                 | V_PRPGP_MEMBROS_BANCA                | Membro             |        |            |                     |                   |                    | ✔️                   | ✔️                    |                         | ✔️              | ✔️                              |                           |                             |
| Projetos               | PM_PROJETOS_PARTICIPANTES            | Participante       |        |            |                     |                   |                    | ✔️                   | ✔️                    |                         |                 |                                 |                           |                             |                           |
| Projetos               | V_PRPGP_PROJETOS_POS                 | Projeto            |        |            |                     |                   |                    |                      |                       |                         |                 |                                 | ✔️                        | ✔️                          |
