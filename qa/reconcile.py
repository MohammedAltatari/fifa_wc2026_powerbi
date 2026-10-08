"""E) Quality check: recompute every number shown in the Power BI screenshots independently with pandas."""
import sys
import pandas as pd, numpy as np
# Usage: python reconcile.py <path to fifa_world_cup_2026_player_performance.csv>
df = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else 'fifa_world_cup_2026_player_performance.csv')
app = df[df.minutes_played > 0]
tm = df.groupby(['match_id', 'team'], as_index=False).agg(
    stage=('tournament_stage', 'first'), stadium=('stadium', 'first'), city=('city', 'first'),
    res=('match_result', 'first'), gf=('goals_team', 'first'), ga=('goals_opponent', 'first'), xg=('expected_goals_xg', 'sum'))
tm['xg'] = tm.xg.round(2); tm['pts'] = tm.res.map({'W': 3, 'D': 1, 'L': 0})
rows = []
def chk(page, item, dax, py):
    rows.append((page, item, dax, py, 'OK' if str(dax) == str(py) else 'MISMATCH'))
f0 = lambda v: f"{v:,.0f}"; f1 = lambda v: f"{v:,.1f}"; f2 = lambda v: f"{v:,.2f}"
p0 = lambda v: f"{v*100:.0f}%"; p1 = lambda v: f"{v*100:.1f}%"
sg = lambda v: f"{v:+.0f}"; sp = lambda v: f"{v*100:+.0f}%"

# ---- Overview
chk('Overview', 'Matches', '1,050', f0(tm.match_id.nunique()))
chk('Overview', 'Total Goals', '2,794', f0(tm.gf.sum()))
chk('Overview', 'Goals per Match', '2.66', f2(tm.gf.sum() / tm.match_id.nunique()))
chk('Overview', 'Players Used', '1,248', f0(app.player_id.nunique()))
chk('Overview', 'Avg Player Rating', '6.29', f2(app.player_rating.mean()))
md = tm.drop_duplicates('match_id')
chk('Overview', 'Draw Rate', '26.3%', p1((md.res == 'D').mean()))
gps = tm.groupby('stage').agg(g=('gf', 'sum'), m=('match_id', 'nunique'))
for st, v in [('Group Stage', '2.66'), ('Round of 32', '2.69'), ('Round of 16', '2.73'), ('Quarter Finals', '2.38'),
              ('Semi Finals', '3.00'), ('Third Place Match', '2.29'), ('Final', '3.00')]:
    chk('Overview', f'Goals per match - {st}', v, f2(gps.loc[st, 'g'] / gps.loc[st, 'm']))
p = df.groupby(['player_id', 'player_name']).agg(G=('goals', 'sum'), A=('assists', 'sum'), Min=('minutes_played', 'sum')).reset_index()
p['rank'] = p.G + p.A / 100 + (p.G * 90 / p.Min) / 10000
top = p.sort_values('rank', ascending=False).head(10)
shown = ['Memphis Zerrouki 24', 'Kasey Hector 16', 'Dominik Kramaric 15', 'Eric Rodriguez 15', 'Mohannad Majeed 15',
         'Vinicius Nunes 15', 'Eric Mba 14', 'Randal Duarte 14', 'Gianluigi Calafiori 13', 'Saleh Al-Qahtani 13']
chk('Overview', 'Top 10 scorers (set)', ', '.join(sorted(shown)), ', '.join(sorted(f"{r.player_name} {r.G}" for r in top.itertuples())))
city = md.groupby('city').size()
for c, v in [('Philadelphia', 82), ('Monterrey', 77), ('Guadalajara', 73), ('Vancouver', 72), ('Atlanta', 71), ('Kansas City', 69),
             ('Houston', 68), ('Dallas', 67), ('Los Angeles', 66), ('San Francisco', 66), ('Seattle', 61), ('Toronto', 61),
             ('Miami', 60), ('East Rutherford', 54), ('Mexico City', 53), ('Boston', 50)]:
    chk('Overview', f'Matches - {c}', str(v), str(city[c]))

# ---- Teams
t = tm.groupby('team').agg(MP=('match_id', 'count'), W=('res', lambda s: (s == 'W').sum()), D=('res', lambda s: (s == 'D').sum()),
                           L=('res', lambda s: (s == 'L').sum()), GF=('gf', 'sum'), GA=('ga', 'sum'), P=('pts', 'sum'), XG=('xg', 'sum'))
def team_row(r):
    return ' '.join([f0(r.MP), f0(r.W), f0(r.D), f0(r.L), p1(r.W / r.MP), f2(r.P / r.MP), f2(r.GF / r.MP), f2(r.GA / r.MP),
                     sg(r.GF - r.GA), f2(r.XG / r.MP)])
for team, v in [('Nigeria', '40 23 10 7 57.5% 1.98 1.70 1.05 +26 0.38'), ('Colombia', '46 24 4 18 52.2% 1.65 1.43 1.33 +5 0.41'),
                ('Brazil', '45 22 11 12 48.9% 1.71 1.62 1.18 +20 0.43'), ('Portugal', '43 21 9 13 48.8% 1.67 1.47 1.33 +6 0.39'),
                ('Belgium', '51 24 11 16 47.1% 1.63 1.55 1.37 +9 0.54'), ('Algeria', '41 19 7 15 46.3% 1.56 1.46 1.24 +9 0.42'),
                ('Jamaica', '59 27 9 23 45.8% 1.53 1.49 1.36 +8 0.35'), ('Austria', '33 13 12 8 39.4% 1.55 1.64 1.30 +11 0.49')]:
    chk('Teams', f'Row - {team} (MP W D L Win% Pts/M GF/M GA/M GD xG/M)', v, team_row(t.loc[team]))
conf = {'CAF': ['Algeria','Cameroon','Egypt','Ghana','Morocco','Nigeria','Senegal','South Africa','Tunisia'],
        'CONMEBOL': ['Argentina','Brazil','Chile','Colombia','Ecuador','Peru','Uruguay'],
        'CONCACAF': ['Canada','Costa Rica','Jamaica','Mexico','Panama','United States'],
        'AFC': ['Australia','Iran','Iraq','Japan','Qatar','Saudi Arabia','South Korea','Uzbekistan']}
tm['conf'] = tm.team.map({tt: c for c, ts in conf.items() for tt in ts}).fillna('UEFA')
cw = tm.groupby('conf').res.apply(lambda s: (s == 'W').mean())
for c, v in [('CONMEBOL', '38.4%'), ('UEFA', '37.3%'), ('CAF', '36.9%'), ('CONCACAF', '36.7%'), ('AFC', '34.6%')]:
    chk('Teams', f'Win % - {c}', v, p1(cw[c]))

# ---- Players
pl = df.groupby('player_id').agg(name=('player_name', 'first'), pos=('position', 'first'), mv=('market_value_eur', 'first'),
                                 Min=('minutes_played', 'sum')).join(app.groupby('player_id').player_rating.mean().rename('r'))
q = pl[pl.Min >= 900].copy(); n = len(q)
x = q.mv / 1e6; chk('Players', 'Value vs rating correlation (900+ min)', '0.73', f2(np.corrcoef(x, q.r)[0, 1]))
q['rp'] = q.r.rank(method='min').sub(1) / (n - 1); q['vp'] = q.mv.rank(method='min').sub(1) / (n - 1); q['gap'] = q.rp - q.vp
for nm, v in [('Marcus Mount', '1.0 6.27 57% 1% +56%'), ('Themba Xoki', '7.9 6.95 91% 41% +50%'), ('Cengiz Gonul', '5.4 6.57 78% 30% +49%'),
              ('Victor Ajayi', '5.3 6.53 77% 29% +48%'), ('Nabil Bennacer', '1.8 6.21 51% 4% +47%'), ('Xherdan Mvogo', '1.7 6.19 49% 3% +46%'),
              ('Leandro Pezzella', '2.1 6.21 50% 6% +45%'), ('Ao Mori', '2.7 6.25 55% 10% +44%'), ('Christian Robinson', '1.4 6.14 45% 2% +43%')]:
    r = q[q.name == nm].iloc[0]
    chk('Players', f'Best value - {nm} (EUR M, rating, rating pct, value pct, gap)', v,
        ' '.join([f1(r.mv / 1e6), f2(r.r), p0(r.rp), p0(r.vp), sp(r.gap)]))
chk('Players', 'Best value - top 9 order', 'Mount, Xoki, Gonul, Ajayi, Bennacer, Mvogo, Pezzella, Mori, Robinson',
    ', '.join(n_.split()[-1] for n_ in q.sort_values('gap', ascending=False).head(9).name))
for pos, v in [('Goalkeeper', '144 6.21 0.03 0.32 1.95 70.0%'), ('Defender', '432 6.24 0.10 0.55 10.90 80.6%'),
               ('Midfielder', '384 6.31 0.32 1.91 5.17 83.7%'), ('Forward', '288 6.36 0.53 1.42 1.70 75.9%')]:
    a = df[df.position == pos]; mins = a.minutes_played.sum()
    got = ' '.join([f0(a[a.minutes_played > 0].player_id.nunique()), f2(a[a.minutes_played > 0].player_rating.mean()),
                    f2((a.goals.sum() + a.assists.sum()) * 90 / mins), f2(a.key_passes.sum() * 90 / mins),
                    f2(a.defensive_actions.sum() * 90 / mins), p1(a.successful_passes.sum() / a.total_passes.sum())])
    chk('Players', f'Position profile - {pos}', v, got)

# ---- Physical
mins = df.minutes_played.sum()
chk('Physical', 'Distance per 90 (km)', '9.9', f1(df.distance_covered_km.sum() * 90 / mins))
chk('Physical', 'Sprint distance per 90 (km)', '1.15', f2(df.sprint_distance_km.sum() * 90 / mins))
chk('Physical', 'Avg top speed (km/h)', '32.3', f1(app.top_speed_kmh.mean()))
chk('Physical', 'Max top speed (km/h)', '37.0', f1(df.top_speed_kmh.max()))
chk('Physical', 'Avg stamina score', '87.0', f1(app.stamina_score.mean()))
for pos, d, s, sp_ in [('Goalkeeper', '8.5', '0.97', '29.0'), ('Defender', '9.6', '1.11', '32.5'), ('Midfielder', '10.8', '1.24', '32.5'), ('Forward', '9.9', '1.15', '32.5')]:
    a = df[df.position == pos]; m_ = a.minutes_played.sum()
    chk('Physical', f'{pos}: distance/90, sprint/90, top speed', f'{d} {s} {sp_}',
        f"{f1(a.distance_covered_km.sum()*90/m_)} {f2(a.sprint_distance_km.sum()*90/m_)} {f1(a[a.minutes_played>0].top_speed_kmh.mean())}")

# ---- Compare + Profile (per-player metrics)
def player_metrics(rows_):
    m_ = rows_.minutes_played.sum(); a_ = rows_[rows_.minutes_played > 0]
    return {'Appearances': len(a_), 'Minutes Played': m_, 'Avg Player Rating': a_.player_rating.mean(),
            'Market Value (EUR M)': rows_.drop_duplicates('player_id').market_value_eur.sum() / 1e6,
            'Goals': rows_.goals.sum(), 'Assists': rows_.assists.sum(),
            'Goals per 90': rows_.goals.sum() * 90 / m_, 'Assists per 90': rows_.assists.sum() * 90 / m_,
            'xG per 90': rows_.expected_goals_xg.sum() * 90 / m_, 'xA per 90': rows_.expected_assists_xa.sum() * 90 / m_,
            'Shots per 90': rows_.shots.sum() * 90 / m_, 'Shot Accuracy %': rows_.shots_on_target.sum() / rows_.shots.sum(),
            'Conversion %': rows_.goals.sum() / rows_.shots.sum(), 'Key Passes per 90': rows_.key_passes.sum() * 90 / m_,
            'Pass Accuracy %': rows_.successful_passes.sum() / rows_.total_passes.sum()}
FMT = {'Appearances': f0, 'Minutes Played': f0, 'Avg Player Rating': f2, 'Market Value (EUR M)': f1, 'Goals': f0, 'Assists': f0,
       'Shot Accuracy %': p1, 'Conversion %': p1, 'Pass Accuracy %': p1}
fmt = lambda k, v: FMT.get(k, f2)(v)
A = player_metrics(df[df.player_name == 'Memphis Zerrouki']); B = player_metrics(df[df.player_name == 'Mohannad Majeed'])
shown = {'Appearances': ('33', '23'), 'Minutes Played': ('2,235', '1,396'), 'Avg Player Rating': ('7.54', '7.61'),
         'Market Value (EUR M)': ('154.4', '71.7'), 'Goals': ('24', '15'), 'Assists': ('9', '10'), 'Goals per 90': ('0.97', '0.97'),
         'Assists per 90': ('0.36', '0.64'), 'xG per 90': ('0.13', '0.14'), 'xA per 90': ('0.06', '0.11'), 'Shots per 90': ('3.30', '3.42'),
         'Shot Accuracy %': ('20.7%', '17.0%'), 'Conversion %': ('29.3%', '28.3%'), 'Key Passes per 90': ('2.62', '2.39'),
         'Pass Accuracy %': ('78.2%', '75.6%')}
for k, (va, vb) in shown.items():
    chk('Compare', f'{k} (Zerrouki | Majeed)', f'{va} | {vb}', f'{fmt(k, A[k])} | {fmt(k, B[k])}')
P = player_metrics(df[df.player_name == 'Aaron Wright'])
fw = df[df.position == 'Forward']; F = player_metrics(fw); nfw = fw[fw.minutes_played > 0].player_id.nunique()
for k in ['Appearances', 'Minutes Played', 'Market Value (EUR M)', 'Goals', 'Assists']: F[k] = F[k] / nfw
prof = {'Appearances': ('35', '27', '+31%'), 'Minutes Played': ('1,842', '1,647', '+12%'), 'Avg Player Rating': ('6.08', '6.36', '-4%'),
        'Market Value (EUR M)': ('13.0', '26.4', '-51%'), 'Goals': ('9', '6', '+44%'), 'Assists': ('5', '3', '+46%'),
        'Goals per 90': ('0.44', '0.34', '+28%'), 'Assists per 90': ('0.24', '0.19', '+30%'), 'xG per 90': ('0.06', '0.11', '-46%'),
        'xA per 90': ('0.02', '0.06', '-68%'), 'Shots per 90': ('1.71', '2.35', '-27%'), 'Shot Accuracy %': ('14.3%', '16.2%', '-12%'),
        'Conversion %': ('25.7%', '14.6%', '+77%'), 'Key Passes per 90': ('1.03', '1.42', '-28%')}
for k, (vp, va, vd) in prof.items():
    chk('Player Profile', f'{k} (Aaron Wright | Forward avg | diff)', f'{vp} | {va} | {vd}',
        f'{fmt(k, P[k])} | {fmt(k, F[k])} | {sp((P[k] - F[k]) / F[k])}')
aw = df[df.player_name == 'Aaron Wright'].iloc[0]
chk('Player Profile', 'Info line', 'Australia | Forward | Age 23 | Ulsan HD | 185 cm | Right foot',
    f"{aw.team} | {aw.position} | Age {aw.age} | {aw.club_name} | {aw.height_cm} cm | {aw.preferred_foot} foot")

out = pd.DataFrame(rows, columns=['Page', 'Check', 'Power BI (DAX)', 'Python (pandas)', 'Result'])
out.to_csv('reconciliation.csv', index=False)
print(out.Result.value_counts().to_dict())
print(out[out.Result != 'OK'].to_string())
