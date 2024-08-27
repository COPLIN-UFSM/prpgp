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
CREATE OR REPLACE VIEW V_PRPGP_VAGAS_INSCRITOS_MATRICULADOS AS (
select pdv.ID_CONCURSO, pdv.ID_CONC_EDICAO, pdv.ID_OPCAO, pdv.ID_CURSO,
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
inner join POS_DADOS_INSCRICAO pdi 
    on pdv.ID_CONCURSO = pdi.ID_CONCURSO and
    pdv.ID_CONC_EDICAO = pdi.ID_CONC_EDICAO and
    pdv.ID_OPCAO = pdi.ID_OPCAO and
    pdv.ID_CURSO = pdi.ID_CURSO
    LEFT JOIN V_PRPGP_TIPOS_COTAS cotas 
        ON cotas.ID_CONC_EDICAO = pdv.ID_CONC_EDICAO AND cotas.CODIGO_COTA = pdv.COD_COTA
    left join (
        select id_candidato, 1 MATRICULOU
    from CURSOS_ALUNOS_ATZ) matr on matr.ID_CANDIDATO = pdi.ID_CANDIDATO
group by 
    pdv.ID_CONCURSO, pdv.ID_CONC_EDICAO, pdv.ID_OPCAO, pdv.ID_CURSO,
    case
        when cotas.CODIGO_COTA is null then 'AC'
        else cotas.CODIGO_COTA
    end,
    pdv.VAGAS_OFERECIDAS
);
```

### Concursos (i.e. processos seletivos)

```sql
create or replace view V_PRPGP_CONCURSOS as (
    select conc.ID_CONCURSO, conc.DESCR_CONCURSO, conc.ANO, conc_ed.ID_CONC_EDICAO, conc_ed.DESCR_CONC_EDICAO
    from bee.CONCURSOS conc
    inner JOIN bee.CONC_EDICOES conc_ed ON conc_ed.ID_CONCURSO = conc.ID_CONCURSO
);
```

## Docentes de pós-graduação com atividade nos últimos 15 anos

```sql
create or replace view V_PRPGP_DOCENTES_POS AS (
    select
        gsu.ID_CONTRATO_RH,
        iserv.MATR_EXTERNA SIAPE,
        iserv.NOME_FUNCIONARIO,
        iserv.SEXO,
        CARGOS_RH.DESCR_CARGO,
        gsu.DT_ADMISSAO_CARGO,
        gsu.DT_DESLIGAMENTO,
        iserv.NACIONALIDADE
    from iserv_geral iserv
    inner join GERAL_SERVIDORES_UFSM gsu on iserv.ID_CONTRATO_RH = gsu.ID_CONTRATO_RH
    inner join CARGOS_RH on gsu.ID_CARGO = CARGOS_RH.ID_CARGO
    where gsu.ID_CONTRATO_RH in (
        select gsu_inner.ID_CONTRATO_RH
        from GERAL_SERVIDORES_UFSM gsu_inner
        inner join TURMAS_DOCENTES td on gsu_inner.ID_CONTRATO_RH = td.ID_DOCENTE
        inner join turmas_vagas tv on td.ID_TURMA = tv.ID_TURMA
        inner join ACAD_CURSOS ac on tv.ID_CURSO = ac.ID_CURSO
        inner join ACAD_NIVEL_CURSOS anc on ac.ID_NIVEL = anc.ID_NIVEL
        inner join ACAD_MODALIDADE am on ac.ID_MODALIDADE = am.ID_MODALIDADE
        where anc.DESCRICAO = 'Pós-Graduação'
        and am.DESCRICAO in ('Mestrado', 'Doutorado')
        and ((year(current_date) - tv.ANO) <= 15)
    )
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
create or replace view V_PRPGP_TURMAS_POS as (
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

## Projetos de cursos ou unidades de pós-graduação

A partir de 2015.

### Projetos

```sql
CREATE OR REPLACE VIEW V_PRPGP_PROJETOS_POS as
SELECT projs.ID_PROJETO,projs.NUM_PROCESSO,projs.TITULO,projs.CLASSIFICACAO,
       BEE.GET_TAB_EST_DESC(projs.SITUACAO_TAB, projs.SITUACAO_ITEM) AS SITUACAO,
       --oinst.COD_ESTRUTURADO,oinst.NOME_UNIDADE,
       --proj_orgaos.FUNCAO,
       projs.DT_INICIAL, projs.DT_CONCLUSAO
FROM PM_PROJETOS_COMPLETO projs
--INNER JOIN PM_PROJETOS_ORGAOS proj_orgaos ON projs.ID_PROJETO = proj_orgaos.ID_PROJETO
--INNER JOIN unidades_pos P ON P.ID_UNIDADE = proj_orgaos.ID_UNIDADE
--INNER JOIN ORG_INSTITUICAO oinst ON oinst.ID_UNIDADE = proj_orgaos.ID_UNIDADE
WHERE projs.DT_REGISTRO >= '01.01.2015';
```

### Unidades executoras/participantes

```sql
CREATE OR REPLACE VIEW V_PRPGP_PROJETOS_POS_ORGAOS AS
WITH unidades_pos AS ( -- cursos de pós-graduação ou coordenadorias de pós-graduação com projetos
    (
        -- coordenadorias
        SELECT inst.ID_UNIDADE
        FROM ORG_INSTITUICAO left_inst
        INNER JOIN CURSOS ON cursos.ID_UNIDADE = left_inst.ID_UNIDADE
        INNER JOIN ORG_INSTITUICAO inst ON inst.ID_UNIDADE = left_inst.ID_UNID_VINC_ADM
        inner join acad_nivel_cursos anc on cursos.NIVEL_CURSO_ITEM = anc.ID_NIVEL
        inner join TAB_ESTRUTURADA te on left_inst.SITUACAO_TAB = te.COD_TABELA and left_inst.SITUACAO_ITEM = te.ITEM_TABELA
        where upper(strip(anc.DESCRICAO)) in ('PÓS-GRADUAÇÃO', 'PROGRAMAS DE PÓS-GRADUAÇÃO')
        and upper(strip(te.DESCRICAO)) in ('A DESATIVAR', 'DESATIVADA', 'EXTINTA')
    ) UNION (
        -- cursos
        SELECT CURSOS.ID_UNIDADE
        FROM CURSOS
        INNER JOIN ORG_INSTITUICAO right_inst ON right_inst.ID_UNIDADE = CURSOS.ID_UNIDADE
        inner join acad_nivel_cursos anc on cursos.NIVEL_CURSO_ITEM = anc.ID_NIVEL
        inner join TAB_ESTRUTURADA te on right_inst.SITUACAO_TAB = te.COD_TABELA and right_inst.SITUACAO_ITEM = te.ITEM_TABELA
        where upper(strip(anc.DESCRICAO)) in ('PÓS-GRADUAÇÃO', 'PROGRAMAS DE PÓS-GRADUAÇÃO')
        and upper(strip(te.DESCRICAO)) in ('A DESATIVAR', 'DESATIVADA', 'EXTINTA')
    )
)
SELECT proj_orgaos.ID_PROJETO, -- projs.NUM_PROCESSO,projs.TITULO,projs.CLASSIFICACAO,
       -- BEE.GET_TAB_EST_DESC(projs.SITUACAO_TAB, projs.SITUACAO_ITEM) AS SITUACAO,
       oinst.COD_ESTRUTURADO,oinst.NOME_UNIDADE,
       proj_orgaos.FUNCAO
       -- projs.DT_INICIAL, projs.DT_CONCLUSAO
FROm PM_PROJETOS_ORGAOS proj_orgaos
INNER JOIN unidades_pos P ON P.ID_UNIDADE = proj_orgaos.ID_UNIDADE
INNER JOIN ORG_INSTITUICAO oinst ON oinst.ID_UNIDADE = proj_orgaos.ID_UNIDADE;
```

### Participantes (CPF)

ver PM_PROJETOS_ORGAOS e participantes_proj

```sql
select *
from PM_PROJETOS_PARTICIPANTES;
```

## Membros de banca externos

```sql
CREATE OR REPLACE VIEW V_PRPGP_MEMBROS_EXTERNOS_BANCAS AS
select
    ID_PARTICIP_PLANO, NOME_PART_EXTERNO, NOME_INST_ORIGEM, SIGLA_INST_ORIGEM, CPF,
    CASE
        WHEN strip(te.descricao) = 'Pós doctor' then 'Doutor'
        WHEN strip(te.DESCRICAO) = 'PHD' then 'Doutor'
        WHEN strip(te.DESCRICAO) = 'Graduado' then 'Graduação'
        else te.DESCRICAO
    END AS TITULACAO
from PARTICIP_PLANO
inner join TAB_ESTRUTURADA te on te.COD_TABELA = TITULACAO_TAB and te.ITEM_TABELA = TITULACAO_ITEM
where ID_CONTRATO_RH is null;
```

## Membros de bancas

```sql
create or replace view V_PRPGP_MEMBROS_BANCA AS
select
    ID_PLANO_ESTUDO,
    CASE
        when PARTIC.ID_CONTRATO_RH is not null then ID_PARTICIP_PLANO
        ELSE NULL
    END AS ID_PARTICIP_PLANO,-- externo
    ID_CONTRATO_RH, -- interno
    NULL AS ID_CURSO_ALUNO, -- id_curso_aluno
    DECODE(partic.TIPO_PARTICIP, 'F', 'Servidor', 'Externo') AS TIPO_VINCULO,
    BEE.GET_TAB_EST_DESC(partic.SITUACAO_TAB, partic.SITUACAO_ITEM) AS SITUACAO,
    GET_TAB_EST_DESC(partic.TIPO_PARTICIP_TAB, partic.TIPO_PARTICIP_ITEM) AS TIPO_PARTICIPANTE
from PARTICIP_PLANO partic
union
select
    ID_PLANO_ESTUDO, NULL AS ID_PARTIC_PLANO, NULL AS ID_CONTRATO_RH, id_curso_aluno,
    'Aluno' AS TIPO_VINCULO, 'Efetivo' as SITUACAO, 'Aluno' as TIPO_PARTICIPANTE
from PLANOS_ESTUDOS plano;
```

## Defesas 

```sql
CREATE OR REPLACE VIEW V_PRPGP_DEFESAS AS
select ID_PLANO_ESTUDO, ID_PROJETO, DH_DEFESA,
    GET_TAB_EST_DESC(planos.SITUACAO_PLANO_TAB, planos.SITUACAO_PLANO_ITEM) AS SITUACAO_PLANO,
    GET_TAB_EST_DESC(planos.SITUACAO_defesa_TAB, planos.SITUACAO_defesa_ITEM) AS SITUACAO_DEFESA
from PLANOS_ESTUDOS planos;
```