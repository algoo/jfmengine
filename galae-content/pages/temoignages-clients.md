---
title Temoignages clients
slug temoignages-clients
lang fr
template_engine jinja2

header_version testimonial
---
{

}
--- BODY ---


{% from "widgets/page_section_reference_logos.html" import page_section_reference_logos %}
{% from "widgets/testimonials.html" import testimonials %}

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

{{testimonials(
    PERSONS = 
    [
        {
            "name": "Dominique Hébert", 
            "job": "Directeur du développement de l'association Educ'AT qui oeuvre pour la prévention du harcèlement scolaire",
            "testimonial" : 
            [
                "Je souhaitais pouvoir offrir une adresse email à chaque membre actif dans l'association sans que ça nous coûte un bras.",
                "Grâce à l'offre Mail de Galae, pour 96 € TTC par an, <strong>je peux créer autant d'adresses email et d'alias que je veux</strong> avec pour seules limites 100 envois par jours et 30 Go au total."
            ],
            "img_url": "assets/img/testimonials/educ-at--dominique-hebert.webp"
        },
        {
            "name": "Lucie ANGLADE", 
            "job": "CourtBouillon (développement de logiciels libres)",
            "testimonial" : 
            [
                "Suite à un important changement tarifaire de notre précédent prestataire, nous recherchions un <strong>service de mails éthique et à prix raisonnable</strong>.",
                "Nous avons choisi de miser sur galae en  participant au crowdfunding et nous sommes très satisfaits du service.",
                "<img class='img-fluid rounded-circle mb-3' style='max-width: 4em; float:right;' src='" ~ static('assets/img/testimonials/court-bouillon.webp') ~ "' alt='' /> Ça marche, <strong>la communication est claire</strong> et les gens sont sympas&nbsp;!"
            ],
            "img_url": "assets/img/testimonials/court-bouillon--lucie-anglade.webp",
        },
        {
            "name": "Mathieu Labonne", 
            "job": "Ecohameau du Plessis (habitat participatif)",
            "testimonial" : 
            [
                "Au sein de notre écohameau, nous cherchions un moyen de créer de nombreuses adresses email, sans avoir besoin de beaucoup de stockage.",
                "Nous étions surpris des prix exorbitants de plusieurs hébergeurs, y
                 compris de celui de notre site internet. Un ami spécialiste de
                 logiciels libres nous a parlé du lancement du service de Galae et
                 <strong>nous avons été accueilli avec beaucoup d'attention et d'écoute</strong>.",
                "L'offre proposé répond énormément à nos besoins.",
                "En tant que collectif citoyen de plusieurs dizaines de personnes
                 ayant besoin de créer des listes de diffusion et des adresses email pour
                 des rôles en interne, l'offre de Galae est vraiment précieuse pour nous
                 et répond à notre petit budget d'association !"
            ],
            "img_url": "assets/img/testimonials/ecohameau-du-plessis--mathieu-labonne.webp"
        },
        {
            "name": "Frédéric ROSAIN", 
            "job": "Entrepreneur et conférencier – Expert numérique responsable et low tech.",
            "testimonial" : 
            [
                "J’apprécie particulièrement de la part de ce service e-mail
                 éthique, <strong>la souplesse de facturation à l’usage
                 effectif</strong>.",
                "En outre, cette offre est très concurrentielle : 20 € par an
                 pour 35 e-mails envoyés par jour, plus l’espace de stockage
                 global et non rattaché à chacune des messageries."
            ],
            "img_url": "assets/img/testimonials/kevin-guerin.webp"
        },
        {
            "name": "Kévin Guérin", 
            "job": "Technicien indépendant dans l'emballage industriel.",
            "testimonial" : 
            [
                "Intéressé par le coté éthique, la proximité, un hébergement en
                 France, en confiance avec la société Algoo, voilà ce qui a
                 motivé mon choix vers Galae.",
                "Très content du service."
            ],
            "img_url": "assets/img/testimonials/f-tech-assistance--frederic-rosain.webp"
        }

    ]
) }}

<!-- Testimonials-->
<section class="testimonials text-center">
    <div class="container">
        <div class="row text-center">
            <p class="lead">
                Vous êtes déjà client ? Vous êtes la meilleure preuve que le service est satisfaisant.
            </p>
            <p class="lead">
                <strong>Faites-nous votre retour</strong> : cela vous prendra moins de 5 minutes et pour nous ce sera un énorme gain !
            </p>
            <p>
                <a class="btn btn-primary" href="#!" onclick="this.href='mailto:hello@galae.net?subject=Galae - j\'utilise le service et voici mon retour !&body=Bonjour,%0D%0A%0D%0AJe suis utilisateur du service e-mail galae et voici mon retour :%0D%0A%0D%0A🗿 Prénom et NOM : ...%0D%0A%0D%0A🏛️ Mon rôle et mon organisation : ...%0D%0A%0D%0A✅ Ce que je trouve bien / ce qui m\'a convaincu dans le service : ...%0D%0A%0D%0A🖼️ lien vers une photo de profil ou photo en pièce jointe :%0D%0A%0D%0A----%0D%0A%0D%0A💬 Remarques et commentaires complémentaires : ...%0D%0A%0D%0A----%0D%0A%0D%0AJe suis d\'accord pour que mon témoignage soit publié sur le site interne de galae.%0D%0A%0D%0AMerci !'">Partager mon ressenti <i class="bi-send"></i></a>
            </p>
        </div>
    </div>
</section>