The agent was able to fully build the app basically from just one good prompt with the SPEC.
Basically all the features were developed besides some parts that I did not specify in the
SPEC like adding more questions and exit codes under certain cases (like if I was not in)
a quiz currently and they CTRL+C or something. So basically 7/8 of the criteria passed
after the first try. The only time I "intervened" during phase two was to tell copilot to add
more questions and not just use the ones that I gave it, which could have easily been fixed by
a more specific SPEC.md. For phase 3, the bugs that copilot caught were little bugs if even bugs,
were mainly just telling the user that they closed the app when they were not currently taking a
quiz. That could also be fixed by specifying the behavior for every case in the SPEC.md. It also
flagged potential issues in the implementation, which I though was cool. For example in many quiz
apps the questions are given randomly, so it flagged it as a warning that the questions were given
in the same order every time instead of randomly ordered. Next time, I would be even more specific
in my SPEC since this time I thought that being this specific was good enough, but next time, I
will probably feed my SPEC to an LLM to see if I missed any edge cases, or didn't mention how to
implement a certain feature. I think this way is better when building bigger projects because
having one agent do everything may take too long or may make it so the singular agent has too much
to remember (too much context). I think it's fine to do singular agent work for a smaller project
even one like this quiz app, but if you're doing a bigger project like a fullstack app, then a
multi-agent workflow may be the best.