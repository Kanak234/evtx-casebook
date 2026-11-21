The included public.csv is a Hayabusa 4.4.0 verbose CSV export from [the public EVTX sample](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES/blob/4ceed2f4706daf601c212a8f91c113dd85349a2c/Command%20and%20Control/DE_RDP_Tunneling_4624.evtx). Its timestamps use the offset written in the CSV. Source artifacts retain their original terms. The project's MIT license covers the casebook code.

Regenerate with Hayabusa 4.4.0 and the rules bundled with its regular release:
```sh
hayabusa dfir-timeline -f DE_RDP_Tunneling_4624.evtx -p verbose -o public.csv -q -w
```
