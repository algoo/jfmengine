---
title   La lib de compression Xz compromise ...
date    2024-04-03T13:13:26+00:00
category Technologie
abstract Une porte dérobée introduite dans la lib de compression Xz a été fortuitement découverte par un développeur PostgreSQL ...
author Damien ACCORSI
---
{
    
}
---

{%markdown%}
La bibliothèque partagée de compression Xz (liblzma) a été compromise par l'un de ses 2 principaux développeurs. Une porte dérobée a été introduite et fortuitement découverte par un développeur du projet PostgreSQL qui [évoque humblement sa découverte sur Mastodon](https://mastodon.social/@AndresFreundTec/112180083704606941) : « I accidentally found a security issue while benchmarking postgres changes »

L'ingéniosité de l'attaque est de passer par un contributeur au long court et par une démarche très ingénieuse ;  [Ytterbium décrit en détail l'attaque dans un long journal publié sur LinuxFR](https://linuxfr.org/users/ytterbium/journaux/xz-liblzma-compromis).

Une fois n'est pas coutume : le problème des dépendances "invisibles" (et pour autant stratégiques) se pose ... 

![Dépendances](https://imgs.xkcd.com/comics/dependency.png)

(source: https://xkcd.com/2347/ )


{%endmarkdown%}