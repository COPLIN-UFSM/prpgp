# TABLES

Esta página descreve as tabelas e views usadas pelos relatórios do Power BI. As tabelas e views são oriundas do banco 
bee da UFSM.

## Cursos de pós-graduação

```sql
CREATE OR REPLACE VIEW V_PRPGP_CURSOS_POS AS (
    select 
        ac.id_curso, AC.COD_CURSO, ac.NOME_CURSO, 
        anc.DESCRICAO NIVEL_CURSO, am.DESCRICAO MODALIDADE_CURSO, acla.DESCRICAO CLASSIFICACAO_CURSO
    from ACAD_CURSOS ac
    inner join ACAD_NIVEL_CURSOS anc on ac.ID_NIVEL = anc.ID_NIVEL
    inner join ACAD_MODALIDADE am on ac.ID_MODALIDADE = am.ID_MODALIDADE
    inner join ACAD_CLASSIFICACAO acla on ac.ID_CLASSIF = acla.ID_CLASSIF
    where anc.DESCRICAO = 'Pós-Graduação'
    and am.DESCRICAO in ('Mestrado', 'Doutorado')
);
```

## Atratividade de cursos

### Tipos de cotas  

```sql
create or replace view V_PRPGP_TIPOS_COTAS as (
    select
        cotas.id_conc_edicao,
        case
            when cotas.COD_COTA is null then 'AC'
            else cotas.COD_COTA
        end as CODIGO_COTA,
        case
            when cotas.DESCR_COTA is null then 'Ampla Concorrência'
            else cotas.DESCR_COTA
        end as TIPO_COTA
    from bee.COTAS_EDICOES cotas
);
```

### Vagas, inscritos e matriculados

```sql
CREATE OR REPLACE VIEW V_PRPGP_VAGAS_INSCRITOS_MATRICULADOS AS
(
select pdv.ID_CONCURSO,
       pdv.ID_CONC_EDICAO,
       pdv.ID_OPCAO,
       pdv.ID_CURSO,
       case
           when cotas.CODIGO_COTA is null then 'AC'
           else cotas.CODIGO_COTA
           end as CODIGO_COTA,
       pdv.VAGAS_OFERECIDAS,
       count(*)   INSCRITOS,
       '?'     as APROVADOS,
       case
           when sum(matr.MATRICULOU) > 0 then sum(MATRICULOU)
           else 0
           end as MATRICULADOS
from POS_DADOS_VAGAS pdv
         inner join
     POS_DADOS_INSCRICAO pdi on pdv.ID_CONCURSO = pdi.ID_CONCURSO and
                                pdv.ID_CONC_EDICAO = pdi.ID_CONC_EDICAO and
                                pdv.ID_OPCAO = pdi.ID_OPCAO and
                                pdv.ID_CURSO = pdi.ID_CURSO
         LEFT JOIN V_PRPGP_TIPOS_COTAS cotas
                   ON cotas.ID_CONC_EDICAO = pdv.ID_CONC_EDICAO AND cotas.CODIGO_COTA = pdv.COD_COTA
         left join (select id_candidato, 1 MATRICULOU
                    from CURSOS_ALUNOS_ATZ) matr on matr.ID_CANDIDATO = pdi.ID_CANDIDATO
group by pdv.ID_CONCURSO, pdv.ID_CONC_EDICAO, pdv.ID_OPCAO, pdv.ID_CURSO,
         case
             when cotas.CODIGO_COTA is null then 'AC'
             else cotas.CODIGO_COTA
             end,
         pdv.VAGAS_OFERECIDAS
);
```

### Concursos (i.e. processos seletivos)

```sql
create or replace view v_prpgp_concursos as (
    select conc.ID_CONCURSO, conc.DESCR_CONCURSO, conc.ANO, conc_ed.ID_CONC_EDICAO, conc_ed.DESCR_CONC_EDICAO
    from bee.CONCURSOS conc
    inner JOIN bee.CONC_EDICOES conc_ed ON conc_ed.ID_CONCURSO = conc.ID_CONCURSO
);
```

## Docentes de pós-graduação com atividade nos últimos 15 anos

```sql
create or replace view V_PRPGP_DOCENTES_POS AS (
    select distinct gsu.ID_CONTRATO_RH,
                    iserv.MATR_EXTERNA SIAPE,
                    iserv.NOME_FUNCIONARIO,
                    iserv.SEXO,
                    CARGOS_RH.DESCR_CARGO,
                    gsu.DT_ADMISSAO_CARGO,
                    gsu.DT_DESLIGAMENTO,
                    iserv.NACIONALIDADE --, ac.NOME_CURSO
    from ISERV_GERAL iserv
             inner join GERAL_SERVIDORES_UFSM gsu on iserv.ID_CONTRATO_RH = gsu.ID_CONTRATO_RH
             inner join CARGOS_RH on gsu.ID_CARGO = CARGOS_RH.ID_CARGO
             inner join TURMAS_DOCENTES td on iserv.ID_CONTRATO_RH = td.ID_DOCENTE
             inner join CURRICULO_ALUNO ca on ca.ID_TURMA = td.ID_TURMA
             inner join cursos_alunos_atz caa on ca.ID_CURSO_ALUNO = caa.ID_CURSO_ALUNO
             inner join acad_cursos ac on caa.ID_CURSO = ac.ID_CURSO
             inner join ACAD_NIVEL_CURSOS anc on ac.ID_NIVEL = anc.ID_NIVEL
             inner join ACAD_MODALIDADE am on ac.ID_MODALIDADE = am.ID_MODALIDADE
    where anc.DESCRICAO = 'Pós-Graduação'
      and am.DESCRICAO in ('Mestrado', 'Doutorado')
      and ((year(current_date) - ca.ANO) <= 15)
      and ((iserv.DT_DESLIGAMENTO is null) or (year(iserv.DT_DESLIGAMENTO) >= year(current_date)))
);
```

## Discentes de pós-graduação com atividade nos últimos 15 anos

* Apenas mestrado e doutorado (**sem** especialização nem residência)
* Últimos 15 anos

```sql
create or replace view V_PRPGP_DISCENTES_POS AS (
    select caa.ID_CURSO_ALUNO,
           caa.MATRICULA,
           caa.NOME_ALUNO,
           caa.ANO_INGRESSO,
           caa.ANO_EVASAO,
           caa.FORMA_EVASAO,
           ac.ID_CURSO,
           ac.NOME_CURSO,
           anc.DESCRICAO NIVEL_CURSO,
           am.DESCRICAO  MODALIDADE_CURSO,
           caa.NACIONALIDADE
    from CURSOS_ALUNOS_ATZ caa
             inner join acad_cursos ac on caa.ID_CURSO = ac.ID_CURSO
             inner join ACAD_NIVEL_CURSOS anc on ac.ID_NIVEL = anc.ID_NIVEL
             inner join ACAD_MODALIDADE am on ac.ID_MODALIDADE = am.ID_MODALIDADE
    where anc.DESCRICAO = 'Pós-Graduação'
      and am.DESCRICAO in ('Mestrado', 'Doutorado')
      and ((year(current_date) - caa.ANO_INGRESSO) <= 15)
);
```

### Disciplinas de pós-graduação

```sql
create or replace view V_PRPGP_DISCIPLINAS_POS as (
    select ID_DISCIPLINA, COD_DISCIPLINA, NOME_DISCIPLINA, CH_TOTAL
    from V_DISCIPLINAS disci
             inner join TAB_ESTRUTURADA est_nivel
                        on disci.NIVEL_CURSO_TAB = est_nivel.COD_TABELA and disci.NIVEL_CURSO_ITEM = est_nivel.ITEM_TABELA
    where est_nivel.DESCRICAO = 'Pós-Graduação'
);
```


## Turmas de pós-graduação dos últimos 15 anos

```sql
create or replace view V_PRPGP_DISCIPLINAS_POS as (
    select td.ID_DOCENTE,
           ca.ID_CURSO_ALUNO,
           ca.ID_ATIV_CURRIC ID_DISCIPLINA,
           ca.ANO            ANO_TURMA,
           td.ENC_DIDATICO   ENCARGO_DIDATICO_DOCENTE
    from CURRICULO_ALUNO ca
             inner join TURMAS_DOCENTES td on ca.ID_TURMA = td.ID_TURMA
    where ((year(current_date) - ca.ANO) <= 15)
);
```