# Trackrecords
This repository is for a web app designed to help people learn how to create accurate trackrecords for a stock portfolio.


https://levelup.gitconnected.com/building-a-membership-system-in-django-under-5-mins-5efd7e03627d
https://www.howtogeek.com/444596/how-to-change-the-default-shell-to-bash-in-macos-catalina/
https://medium.com/geekculture/setting-up-python-environment-in-macos-using-pyenv-and-pipenv-116293da8e72
https://pipenv-fork.readthedocs.io/en/latest/basics.html
https://gist.github.com/rahularity/86da20fe3858e6b311de068201d279e3
https://gist.github.com/rahularity/86da20fe3858e6b311de068201d279e3
https://dev.to/danilovmy/how-to-solve-the-singleton-problem-in-django-modeladmin-g42

https://github.com/typeddjango/django-stubs
https://gearheart.io/articles/overriding-queryset-in-django/

https://steelkiwi.com/blog/best-practices-working-django-models-python/

https://www.agiliq.com/blog/2017/12/django-20-window-expressions-tutorial/

https://testdriven.io/blog/django-debugging-vs-code/

https://www.tradelikeamachine.com/algorithmic-trading-systems/trade-like-a-machine-track-record

https://books.agiliq.com/projects/django-orm-cookbook/en/latest/random.html?highlight=insert#how-to-efficiently-select-a-random-object-from-a-model

https://www.census.gov/naics/reference_files_tools/2022_NAICS_Manual.pdf

https://www.census.gov/naics/?48967

https://library.nyu.edu/

https://dev.to/danilovmy/how-to-solve-the-singleton-problem-in-django-modeladmin-g42

https://stackoverflow.com/questions/28227371/how-to-add-a-running-count-to-rows-in-a-streak-of-consecutive-days

https://pypi.org/project/django-cte/

<!-- SELECT
    *,
    CASE
        WHEN result_type <> prev_result THEN id
        ELSE LAG(id, streak_length::int - 1) OVER (ORDER BY exit_stamp)
    END streak_index
FROM (
    SELECT
        *,
        LAG(result_type, 1, 'N/A') OVER (ORDER BY exit_stamp) as prev_result,
        ROW_NUMBER() OVER (PARTITION BY result_type ORDER BY exit_stamp) - 1 as streak_length
    FROM trackrecord_position
    WHERE portfolio_id = 1 AND position_status = 'closed'
) as cte
ORDER BY id -->