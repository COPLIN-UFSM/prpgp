# Bus Matrix

A bus matrix mostra o relacionamento de tabelas em um modelo relacional, indicando quais medidas estão contidas.

FATOS NAS LINHAS
DIMENSÕES NAS COLUNAS

| Processo de negócio    | Tabela                               | 	Granularidade | Medida | Calendário |   |   |   |   |   |   
|:-----------------------|:-------------------------------------|:---------------|:-------|:-----------|:--|:--|:--|:--|:--|
| Cursos                 | V_PRPGP_CURSOS_POS                   | Curso          |        |            |   |   |   |   |   |
| Docentes               | V_PRPGP_DOCENTES_POS                 | Docente        |        |            |   |   |   |   |   |
| Discentes              | V_PRPGP_DISCENTES_POS                | Discente       |        |            |   |   |   |   |   |
| Atratividade de cursos | V_PRPGP_TIPOS_COTAS                  |                |        |            |   |   |   |   |   |
| Atratividade de cursos | V_PRPGP_VAGAS_INSCRITOS_MATRICULADOS |                |        |            |   |   |   |   |   |
| Atratividade de cursos | V_PRPGP_CONCURSOS                    |                |        | :check:    |   |   |   |   |   |
| Disciplinas            | V_PRPGP_DISCIPLINAS_POS              | Disciplina     |        |            |   |   |   |   |   |
| Turmas                 | V_PRPGP_TURMAS_POS                   | Turma          |        |            |   |   |   |   |   |
| Projetos               | V_PRPGP_PROJETOS_POS                 |                |        |            |   |   |   |   |   |
| Projetos               | V_PRPGP_PROJETOS_POS_ORGAOS          |                |        |            |   |   |   |   |   |
| Projetos               | PM_PROJETOS_PARTICIPANTES            |                |        |            |   |   |   |   |   |
| Bancas                 | V_PRPGP_MEMBROS_EXTERNOS_BANCAS      |                |        |            |   |   |   |   |   |
| Bancas                 | V_PRPGP_MEMBROS_BANCA                |                |        |            |   |   |   |   |   |
| Bancas                 | V_PRPGP_DEFESAS                      |                |        |            |   |   |   |   |   |
