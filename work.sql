instr(column, 'cats')

-- wf with distinct accents
select wf, accent, count(distinct accent)
from wf
group by wf.wf
having count(distinct accent) > 1
order by 3 desc

select wf, accent, count(distinct accent)
from wf
where instr(accent, '"') > 0
group by wf.wf
having count(distinct accent) > 1
order by 3 desc

-- all wfs with distinct accents (84000)
select distinct wf.wf, wf.accent 
from wf, (
  select wf
  from wf
  where instr(accent, '"') > 0
  group by wf.wf
  having count(distinct accent) > 1) as acc
where wf.wf = acc.wf

-- all words with distinct accents
select wf.* from wf, (select wf, accent, count(distinct accent)
from wf
group by wf.wf
having count(distinct accent) > 1) d
where d.wf = wf.wf
order by wf.wf,  wf.fk_inf

-- 
select * from wf 
where wf = 'ківі'

-- wf without accent
select accent
from wf
where instr(accent, '"') = 0

select distinct fid
from wf
where instr(accent, '"') = 0