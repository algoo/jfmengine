--- METADATA (first) ---
title   galae - ethical and free pay-per-use e-mail
slug    en-index
description galae est un service e-mail éthique et libre facturé à l'usage. Toutes nos offres incluent des boîtes emails et domaines illimités hébergés en France.
language    French
lang        en
version .en
engine jinja2
# open graph metatada
og:title        galae - ethical and free pay-per-use e-mail
og:description  galae est un service e-mail éthique et libre facturé à l'usage. Toutes nos offres incluent des boîtes emails et domaines illimités hébergés en France.
og:type         website
og:site_name    galae.net
og:url          https://www.galae.net/fr/
og:image        https://www.galae.net/assets/img/galae_logo.png
og:locale       fr

--- DATA (second JSON Structure) ---
{

}
--- BODY (last / third) ---


{% from "widgets/page_block_h2_with_ul_content_and_image_left.html" import page_block_h2_with_ul_content_and_image_left %}
{% from "widgets/page_block_h2_with_ul_content_and_image_right.html" import page_block_h2_with_ul_content_and_image_right %}
{% from "widgets/page_section_reference_logos.html" import page_section_reference_logos %}
{% from "widgets/page_block_h2_with_content_and_primary_secondary_cta.html" import page_block_h2_with_content_and_primary_secondary_cta%}
{% from "widgets/testimonials_quotes.html" import testimonials_quotes%}
{% from "widgets/page_section_main_cta.html" import page_section_main_cta%}
{% from "widgets/page_block_h2_with_content_dark_background_no_cta.html" import page_block_h2_with_content_dark_background_no_cta%}



{{ page_section_reference_logos(
    REFERENCES = 
    [
        {'name': 'oslandia', 'logo_url': 'assets/img/references/oslandia.webp'},
        {'name': 'narm-pc', 'logo_url': 'assets/img/references/narm-pc.svg'},
        {'name': 'domeo-conseils', 'logo_url': 'assets/img/references/domeo-conseils.webp'},
        {'name': 'ethicsys', 'logo_url': 'assets/img/references/ethicsys.webp'},
        {'name': 'pixngraph', 'logo_url': 'assets/img/references/pixngraph.webp'},
        {'name': '15-09-consulting', 'logo_url': 'assets/img/references/15-09-consulting.webp'},
        {'name': 'apeiron-technology', 'logo_url': 'assets/img/references/apeiron-technology.webp'},
        {'name': 'arundo-tech', 'logo_url': 'assets/img/references/arundo-tech.webp'},
        {'name': 'association-la-granja', 'logo_url': 'assets/img/references/association-la-granja.webp'},
        {'name': 'association-tostaky', 'logo_url': 'assets/img/references/association-tostaky.webp'},
        {'name': 'astrolabe-cae', 'logo_url': 'assets/img/references/astrolabe-cae.webp'},
        {'name': 'asvola', 'logo_url': 'assets/img/references/asvola.webp'},
        {'name': 'back2data', 'logo_url': 'assets/img/references/back2data.webp'},
        {'name': 'bag-era', 'logo_url': 'assets/img/references/bag-era.webp'},
        {'name': 'cositrex', 'logo_url': 'assets/img/references/cositrex.webp'},
        {'name': 'dembell', 'logo_url': 'assets/img/references/dembell.webp'},
        {'name': 'ecohameau-du-plessis', 'logo_url': 'assets/img/references/ecohameau-du-plessis.webp'},
        {'name': 'educat', 'logo_url': 'assets/img/references/educat.webp'},
        {'name': 'elycoop', 'logo_url': 'assets/img/references/elycoop.webp'},
        {'name': 'ethicsys', 'logo_url': 'assets/img/references/ethicsys.webp'},
        {'name': 'keyox', 'logo_url': 'assets/img/references/keyox.webp'},
        {'name': 'la-bataille-du-libre', 'logo_url': 'assets/img/references/la-bataille-du-libre.webp'},
        {'name': 'le-mignon', 'logo_url': 'assets/img/references/le-mignon.webp'},
        {'name': 'les-paysans-du-bocage', 'logo_url': 'assets/img/references/les-paysans-du-bocage.webp'},
        {'name': 'manajet', 'logo_url': 'assets/img/references/manajet.webp'},
        {'name': 'paquerette', 'logo_url': 'assets/img/references/paquerette.webp'},
        {'name': 'sempiternelia-humanites-numeriques', 'logo_url': 'assets/img/references/sempiternelia-humanites-numeriques.webp'},
        {'name': 'spirale-coop', 'logo_url': 'assets/img/references/spirale-coop.webp'},
        {'name': 'tele-mille-vaches', 'logo_url': 'assets/img/references/tele-mille-vaches.webp'},
        {'name': 'ville-ayn', 'logo_url': 'assets/img/references/ville-ayn.webp'},
        {'name': 'ville-dullin', 'logo_url': 'assets/img/references/ville-dullin.webp'},
        {'name': 'fc_home', 'logo_url': 'assets/img/references/fc_home.webp'},
    ]
) }}



<section class="showcase">
    <div class="container-fluid p-0">


{{ page_block_h2_with_ul_content_and_image_right( 
    TITLE = 
    "
        <h2>E-mails <span class='galae-color'>delivered</span>, in line with <span class='galae-color'>standards</span></h2>
    ",
    IMAGE_URL = "assets/img/undraw_futuristic_interface_re_0cm6.svg",
    CONTENT_ITEMS = 
    [
        "Our platform natively supports DKIM, SPF and DMARC.",
        "Interact with your e-mails, address books and calendars via IMAP, POP3, CalDAV and CardDAV standard protocols.",
        "We offer SIEVE filters, aliases and fine-tuned quota management.",
        "We pay close attention to the deliverability of your e-mails."
    ],
    CTA_LABEL = "Découvrir les tarifs",
    CTA_URL = "#pricing"
) }}


{{ page_block_h2_with_ul_content_and_image_left(
    TITLE = "Vos données en <span class='galae-color'>sécurité</span>",
    IMAGE_URL = "assets/img/undraw_relaxation_re_ohkx.svg",
    CONTENT_ITEMS =
    [
        "Notre infrastructure est exclusivement localisée en France.",
        "Nous respectons le RGPD et veillons à le respecter dans la durée. Nous sommes accompagnés par un cabinet spécialisé : <a href='https://www.cosipe.fr/' target='_blank'>Cosipé</a>.",
        "Notre infrastructure matérielle redondée permet d'assurer la pérennité de vos données.",
        "Vos données sont sauvegardées hors-site ; les sauvegardes sont redondées."
    ],
    CTA_LABEL = "Découvrir les tarifs",
    CTA_URL = "#pricing" 
) }}


{{ page_block_h2_with_ul_content_and_image_right( 
    TITLE = "Vous êtes <span class='galae-color'>autonomes</span>, accompagnés et souverains.",
    IMAGE_URL = "assets/img/undraw_experts_re_i40h.svg",
    CONTENT_ITEMS =
    [
        "Interface de gestion fine de votre messagerie : création/suppression de boîtes e-mail, alias, filtres SIEVE, quotas, etc.",
        "<a href=\"https://public-community.galae.net\" target=\"_blank\">Plateforme</a> d'entraide communautaire.",
        "En option : <abbr title=\"Garantie de Temps d'Intervention\">GTI</abbr>, support téléphonique professionnel.",
        "Nous n'utilisons que des logiciels libres et des protocoles ouverts pour assurer l'interopérabilité."
    ],
    CTA_LABEL = "Découvrir les tarifs",
    CTA_URL = "#pricing" 
) }}


    </div>
</section>



{{ page_block_h2_with_content_and_primary_secondary_cta(
    HTMLID = "pricing",
    TITLE = "Offres et tarifs",
    CONTENT = "L'offre galae repose sur les 4 offres suivantes :",
    MAIN_IMG_URL = "assets/img/grille_tarifaire_galae_fr.png",
    MAIN_IMG_ALT = "prix de galae",
    SECONDARY_CTA_URL = "assets/docs/grille_tarifaire_galae.pdf",
    SECONDARY_CTA_TARGET = "_blank",
    SECONDARY_CTA_LABEL = "Téléchargez la grille tarifaire",
    PRIMARY_CTA_URL = "https://pay.galae.net/",
    PRIMARY_CTA_TARGET = "_blank",
    PRIMARY_CTA_LABEL = "Souscrivez maintenant",
    PRIMARY_CTA_ICON = "bi-rocket"
) }}



{{ testimonials_quotes(
    PERSONS =
    [
        { "name": "Dominique Hébert", "job": "Directeur du développement Educ'AT", "testimonial": "Je peux créer autant d'adresses email et d'alias que je veux.", "img_url": "assets/img/testimonials/educ-at--dominique-hebert.webp" },
        { "name": "Mathieu Labonne", "job": "Ecohameau du Plessis", "testimonial": "Nous avons été accueillis avec beaucoup d'attention et d'écoute.", "img_url": "assets/img/testimonials/ecohameau-du-plessis--mathieu-labonne.webp" },
        { "name": "Kévin Guérin", "job": "Entrepreneur et conférencier", "testimonial": "J’apprécie particulièrement la souplesse de facturation à l’usage effectif.", "img_url": "assets/img/testimonials/kevin-guerin.webp" }
    ]

) }}



{{ page_block_h2_with_content_dark_background_no_cta( 
    TITLE = "Pourquoi j'ai décidé de créer le service <span class=\"galae-color\">galae</span> ?",
    CONTENT = 
    "
        <p class='lead'>
            Comme nombre d'entre vous, j'ai constaté une dégradation progressive de la qualité des services e-mail et une augmentation des tarifs.
        </p>
        <p class='lead'>
            Cette conjoncture et les projets que nous menons avec <a href='https://www.algoo.fr' target='_blank'>algoo</a>
            pour le compte de nos clients m'ont décidé à lancer un service e-mail conforme aux standards,
            s'appuyant exclusivement sur des logiciels libres et évidemment respectueux
            des données des utilisateurs.
        </p>
        <p class='lead'>
            Lorsque je les ai interrogés, les clients m'ont demandé :
        </p>
        <ul class='lead'>
        <li>
            un service souple facturé à l'usage effectif &mdash; indexé sur le volume de stockage et le volume d'envoi,
        </li>
        <li>
            une relation de proximité et de confiance qui se matérialise par un vrai support client, humain, de proximité,
        </li>
        <li>
            la mise à disposition d'outils permettant une gestion autonome des boîtes e-mail.
        </li>
        </ul>
        <p class='lead'>
            Nous avons construit le service avec l'équipe, avec la communauté, avec nos clients, pour nos clients.
        </p>
        <p class='lead'>
            Et ça continuera d'être ainsi.
        </p>
        <p class='lead'>
            Décrié, le mail reste la colonne vertébrale de la majorité des systèmes d'informations.

            Nous &mdash; algoo &mdash; sommes là pour vous accompagner dans cette aventure avec notre service de
            <span class='galae-color'>G</span>estion
            <span class='galae-color'>A</span>utonome et
            <span class='galae-color'>L</span>ibre
            d'<span class='galae-color'>A</span>dresses
            <span class='galae-color'>E</span>mail.
        </p>
        <div class='text-end'>
            <img class='img-fluid rounded-circle mb-3' style='max-width: 4em;' src='" ~ static('assets/img/damien-accorsi-algoo-galae.jpg') ~ "' alt='Damien ACCORSI, dirigeant algoo et créateur galae' />
            <h5>Damien ACCORSI</h5>
            <h6>Dirigeant <span class='galae-color'>algoo</span> et créateur de <span class='galae-color'>galae</span></h6>
        </div>
"
) }}



{{ page_section_main_cta(
    HTMLID = "signup",
    TITLE = "Convaincus que vous avez besoin d'un email éthique facturé à l'usage&nbsp;?",
    SUBTITLE =
    "
        <a href=\"https://pay.galae.net/\" target=\"_blank\" class=\"btn btn-primary btn-lg\">
            Souscrivez à galae maintenant&nbsp;!<i class=\"bi-rocket\"></i>
        </a>
    ",
    SECONDARY_TITLE = 
    "
        <p>
            <br/><br/>Vous pouvez aussi 
            <a class=\"signup__link\" href=\"#!\" onclick=\"this.href='mailto:bonjour@algoo.fr?subject=Hello, j\\'aimerais en savoir plus sur vos offres e-mail galae...'\">nous envoyer un e-mail</a>
            ou nous appeler au <a class=\"signup__link\" href=\"tel:+33972497220\">+33 (0)9.72.49.72.20</a>
        </p>
    "
) }}
