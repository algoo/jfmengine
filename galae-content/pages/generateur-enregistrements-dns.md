---
title generateur-enregistrements-dns
description galae est un service e-mail éthique et libre facturé à l'usage. Toutes nos offres incluent des boîtes e-mails et domaines illimités hébergés en France.
slug generateur-enregistrements-dns
language French
lang fr
engine jinja2
header_version genenrdns

og:title        galae - le service e-mail éthique et libre facturé à l'usage
og:description  Cette page vous aide à générer les enregistrements DNS pour vos noms de domaines
og:type         website
og:site_name    galae.net
og:url          https://www.galae.net/fr/
og:image        https://www.galae.net/assets/img/galae_logo.png
og:locale       fr
---
{

}

---

<!DOCTYPE html>
<html lang="en">

    <body>

        <section class="testimonials bg-light">
            <div class="container">

              <div class="row">
                <div class="col-12">
                  <h2 id="configure-dkim">1 &mdash; Configurez DKIM</h2>

                  <div class="card help-text">
                    <div class="card-body">
                      <div class="card-text">
                        <p>
                          <i class="bi bi-lightbulb"></i>
                          galae applique une signature DKIM aux e-mails que vous envoyez.
                        </p>
                        <p>
                          Ajouter la clé publique DKIM dans vos enregistrements DNS permet
                          aux destinataires de vérifier cette signature.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-12 mt-3">
                  <label for="dkimValue" class="form-label">
                    Copiez-collez ci-dessous le contenu du champ <mark>dkim._domainkey</mark> que vous trouvez dans&nbsp;
                    <a href="#" class="btn btn-link btn-sm" target="_blank" id="galaeAdminLink">votre interface de gestion galae</a>.
                    Il s'agit de la chaîne commençant par <mark>v=DKIM1;k=rsa;</mark>.
                  </label>
                  <textarea class="form-control form-control-sm" name="dkimValue" id="dkimValue" cols="50" rows="3"></textarea>
                </div>
              </div>

              <div class="row mt-4">
                <div class="col-12">
                  <h2>2 &mdash; Configurez DMARC</h2>
                  <div class="card help-text">
                    <div class="card-body">
                      <div class="card-text">
                        <i class="bi bi-lightbulb"></i>
                          DMARC aide les systèmes de réception de courriers électroniques à
                          reconnaître qu'un e-mail ne provient pas d'un domaine approuvé.
                          Il conseille au système de réception la manière de traiter ce type d'e-mail.
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-12 mt-3">
                  <fieldset class="form-group">
                    <legend>Politique DMARC à appliquer</legend>
                    <p>
                      Plus la politique sera stricte, moins il risque d'y avoir de spam en votre nom.
                      Une politique stricte nécessite cependant que vous soyez rigoureux sur la
                      configuration de vos envois d'e-mail (notamment depuis les serveurs, les
                      formulaires de contact de votre site web, etc)
                    </p>
                    <div class="form-check">
                      <input class="form-check-input" type="radio" name="dmarkPolicy" id="dmarcPolicyNone" value="none">
                      <label class="form-check-label" for="dmarcPolicyNone">
                        Pas de politique DMARC
                        <small class="form-text text-muted">
                          &mdash; les e-mails envoyés en votre nom et ne validant pas DMARC seront acceptés normalement
                          par vos interlocuteurs.
                        </small>
                      </label>
                    </div>
                    <div class="form-check">
                      <input class="form-check-input" type="radio" name="dmarkPolicy" id="dmarcPolicyQuarantine" value="quarantine" checked>
                      <label class="form-check-label" for="dmarcPolicyQuarantine">
                        Politique de mise en quarantaine
                        <small class="form-text text-muted">
                          &mdash; les e-mails envoyés en votre nom et ne validant pas DMARC seront mis en quarantaine dans la boîte de vos interlocuteurs.
                          Ils pourront tout de même les consulter dans leur dossier SPAM.
                        </small>
                      </label>

                    </div>
                    <div class="form-check disabled">
                      <input class="form-check-input" type="radio" name="dmarkPolicy" id="dmarcPolicyReject" value="reject">
                      <label class="form-check-label" for="dmarcPolicyReject">
                        Politique stricte de rejet
                        <small class="form-text text-muted">
                          &mdash; les e-mails envoyés en votre nom et ne validant pas DMARC seront rejetés avant
                          d'arriver jusqu'à vos interlocuteurs.

                          Cette politique est la plus stricte vis à vis du spam. C'est la moins tolérante si
                          vous avez des serveurs mal configurés qui vous envoient des e-mails.
                          <br/>
                          <mark>Note : en étant trop strict, vos interlocuteurs risquent de ne
                            jamais recevoir vos e-mails.</mark>
                        </small>
                      </label>
                    </div>
                  </fieldset>
                </div>
              </div>

              <div class="row">
                <div class="col-12 mt-3">
                  <label for="dmarkRuaEmail" class="form-label">
                    <fieldset class="form-group">
                      <legend>Adresse e-mail pour recevoir les rapports RUA</legend>
                    </fieldset>
                    <p>
                      Les rapports RUA fournissent une vue de l'ensemble du trafic sur votre domaine.
                      Si vous renseignez une adresse e-mail, les destinataires d'e-mails semblant
                      provenir de votre domaine vous enverront régulièrement des rapports RUA.
                    </p>
                  </label>
                  <input type="email" class="form-control form-control-sm" name="dmarkRuaEmail" id="dmarkRuaEmail" placeholder="Adresse e-mail à laquelle vous souhaitez que les rapports RUA soient envoyés">
                </div>
              </div>

              <div class="row">
                <div class="col-12 mt-4">
                  <h2>3 &mdash; Générez vos enregistrements DNS</h2>
                </div>
              </div>

              <div class="row">
                <div class="col-12 mt-4">
                  <p>Une fois vos enregistrements DNS générés, vous pourrez les copier ci-dessous
                    et les coller dans votre interface de gestion DNS
                  </p>
                  <div class="card help-text">
                    <div class="card-body">
                      <div class="card-text">
                        <p>
                          <i class="bi bi-lightbulb"></i>
                          Attention à ne pas avoir de doublon avec des enregistrements DNS
                          sensiblement identique !
                        </p>
                        <p>
                          Les enregistrement MX à appliquer ne doivent correspondre qu'a ceux
                          fournis ci-dessous pour éviter toute collision avec d'autres fournisseurs e-mail.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-12 mt-4">
                  <div class="col-sm-10">
                    <button class="btn btn-primary" onclick="fillDnsRecord();">Générer mes enregistrements DNS</button>
                  </div>
                </div>
              </div>


              <div class="form-group row mt-4">
                <div class="col-sm-12">
                  <textarea class="form-control" id="dnsRecords" cols="100" rows="20">
                  </textarea>
                </div>
              </div>

            <div class="row">
              <div class="col-12 mt-4">
                Après avoir copié/collé vos enregistrements DNS, vous pouvez fermer cette page.
              </div>
            </div>
          </div>
        </div>
      </section>
        <!-- Call to Action-->
        <section class="call-to-action text-white text-center" id="signup">
            <div class="container position-relative">
                <div class="row justify-content-center">
                    <div class="col-xl-6">
                        <h2 class="mb-4">
                            Vous n'êtes pas encore client ?
                        </h2>
                        <a href="https://pay.galae.net/" target="_blank" class="btn btn-primary btn-lg">
                            Souscrivez à galae maintenant&nbsp;!
                            <i class="bi-rocket"></i>
                        </a>
                    </div>
                </div>
            </div>
        </section>



        <!-- Bootstrap core JS-->
        <script src="{{ static('js/bootstrap.bundle.min.js') }}"></script>
        <!-- Core theme JS-->
        <script src="{{ static('js/scripts.js') }}"></script>
        <!-- Matomo -->
        <script>
          var _paq = window._paq = window._paq || [];
          /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
          _paq.push(['trackPageView']);
          _paq.push(['enableLinkTracking']);
          (function() {
            var u="https://matomo.algoo.fr/";
            _paq.push(['setTrackerUrl', u+'matomo.php']);
            _paq.push(['setSiteId', '10']);
            var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
            g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
          })();
        </script>
        <noscript><p><img src="https://matomo.algoo.fr/matomo.php?idsite=10&amp;rec=1" style="border:0;" alt="" /></p></noscript>
        <!-- End Matomo Code -->
        <script>

          function getDomainName() {
              var domainName = document.querySelector('input[name="domainName"]').value.replace('www.', '').toLowerCase();
              return domainName
          }

          function getGalaeAdminUrl(domainName) {
              return 'https://mail.galae.net/edit/domain/' + domainName
          }


          function fillDnsRecord() {
             var ruaEmail = document.querySelector('input[name="dmarkRuaEmail"]').value.trim();
             var dmarcPolicy = document.querySelector('input[name="dmarkPolicy"]:checked').value.trim();
             var dkimValue =  document.querySelector('textarea[name="dkimValue"]').value.trim();

             // INFO - D.A. - 2024-02-28
             // split DKIM value in substrings of 160 char max. This is required at least for gandi
             // Cf. https://docs.gandi.net/en/domain_names/faq/record_types/txt_record.html
             // Cf. https://en.wikipedia.org/wiki/TXT_record#Format
             var dkimString = ""
             for (const dkimItem of dkimValue.match(/.{1,160}/g)) {
                 dkimString = dkimString + "\"" + dkimItem + "\" ";
             }
             dkimString = dkimString.trim();

             var ruaString = ""
             if(ruaEmail !== "") {
               ruaString = "rua=mailto:"+ruaEmail
             }
             var dnsRecords = `@ 10800 IN MX 10 smtpin-01.galae.net.
@ 10800 IN MX 50 smtpin-02.galae.net.
@ 10800 IN TXT "v=spf1 include:spf.galae.net ?all"
dkim._domainkey 10800 IN TXT ${dkimString}
_dmarc 10800 IN TXT "v=DMARC1; p=${dmarcPolicy}; ${ruaString}"
_autodiscover._tcp 10800 IN SRV 0 1 443 mail.galae.net.
_caldavs._tcp 10800 IN SRV 0 1 443 mail.galae.net.
_caldavs._tcp 10800 IN TXT "path=/SOGo/dav/"
_carddavs._tcp 10800 IN SRV 0 1 443 mail.galae.net.
_carddavs._tcp 10800 IN TXT "path=/SOGo/dav/"
_imap._tcp 10800 IN SRV 0 1 143 mail.galae.net.
_imaps._tcp 10800 IN SRV 0 1 993 mail.galae.net.
_pop3._tcp 10800 IN SRV 0 1 110 mail.galae.net.
_pop3s._tcp 10800 IN SRV 0 1 995 mail.galae.net.
_sieve._tcp 10800 IN SRV 0 1 4190 mail.galae.net.
_smtps._tcp 10800 IN SRV 0 1 465 mail.galae.net.
_submission._tcp 10800 IN SRV 0 1 587 mail.galae.net.
autoconfig 10800 IN CNAME mail.galae.net.
autodiscover 10800 IN CNAME mail.galae.net.`;
              console.log(dnsRecords);
            document.querySelector("#dnsRecords").value = dnsRecords;
          }

          </script>
          
    </body>
</html>