---
title   Quels logiciels libres pour manipuler des fichiers PDF ?
date    2024-05-03T08:43:47+00:00
category univers du libre
abstract Manipuler des fichiers PDF est chose courante ; il existe une série de logiciels libres qui permet de procéder à la majorité des manipulations que l'on est en droit d'attendre de tels outils.
author Damien ACCORSI
---
{
    
}
---

{%markdown%}
Nous sommes tous amenés, à un moment ou à un autre, dans notre vie personnelle ou professionnelle, à manipuler des PDF.

Tout le monde connait Acrobat Reader et autres services en ligne tels que Ilovepdf.

Mais existe-t-il des logiciels libres pour procéder aux même opérations ? Si oui quels sont ces outils ?


## Consulter des PDF 

**Evince** est un visionneur de documents pour GNOME. Il permet de visualiser des PDFs et de les imprimer

## Modifier et produire des PDF

**Libreoffice** permet d'exporter les documents que l'on rédige en PDF.

Moins connu, **Libreoffice Draw** permet quant à lui d'ouvrir des PDF existant et d'en éditer le contenu.

## Découper, extraire, fusionner des fichiers PDF en masse (en ligne de commande)

PDFtk permet facilement de découper un fichier PDF via la commande `pdftk file.pdf burst`

Il est également possible d'extraire un lot de pages `pdftk file.pdf cat 3-5 output pages-3-to-5.pdf`

Enfin, il est possible de concaténer des fichiers PDF, exemple : `pdftk file1.pdf file2.pdf cat output file1-file2-merged.pdf`

D'autres opérations sont possibles.

Pour un équivalent graphique, je vous renvoie vers PDF Chain qui m'a permis, par exemple, de découvrir qu'on pouvait intégrer des pièces jointes quelconques dans un PDF.


![](/actualites/images/500x500/image-b0158969619b6e2215ff928a68a0cd882228d06a.png)

## Découper, extraire, fusionner des PDFs naturellement

Pour un usage plus grand public, je ne peux que vous conseiller de vous tourner vers PDF Arranger.

Il permet de procéder aux même opérations que les outils précédemment cités, avec l'avantage de travailler sur des éléments visuels car l'interface intègre une prévisualisation des pages, une sélection à la souris et des menus contextuels - bref un ensemble plus intuitif pour les utilisations qui ne sont pas familiers avec la ligne de commande.

![](/actualites/images/500x500/image-3a7f8c0e10a091e5b7d8d5ac1d454ff27f1edf6d.png)

----

Voilà, vous savez désormais quoi utiliser pour :


- 🖨 Imprimer un document PDF
- ⤵ tourner les pages d'un document PDF
- ✂ découper un document PDF page par page
- 🖇 fusionner plusieurs documents PDF
- 🔎 extraire des sections de pages d'un document PDF


Vous n'avez plus aucune excuse pour diffuser des données confidentielles sur des services en ligne "gratuits" ;)


{%endmarkdown%}