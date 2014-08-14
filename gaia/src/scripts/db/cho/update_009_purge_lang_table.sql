delete from language where language.psmid in (
-- all psmid's that only have 'English' language
select distinct language.psmid
from (
-- count of how many language entires a psmid has
select item_lang_count.psmid, count(item_lang_count.psmid) as psmid_count
    from (
    -- find out which language a psmid has, and how many times it occurs
    SELECT language.psmid as psmid, language.lang as lang, count(language.lang) as lang_count
    FROM public.language
    group by language.psmid, language.lang
    order by language.psmid, language.lang, count(language.lang)
    ) as item_lang_count
group by item_lang_count.psmid, item_lang_count.psmid
order by count(item_lang_count.psmid) desc
) as psmid_lang_count
inner join language
on language.psmid=psmid_lang_count.psmid
where psmid_lang_count.psmid_count = 1 and lang = 'English')
