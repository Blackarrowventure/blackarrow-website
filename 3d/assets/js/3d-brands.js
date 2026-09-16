/* Black Arrow 3D — single source of truth for the brand list.
   Every brand selector on the site (nav dropdown, shop filter, product
   data validation) reads from this array so adding/removing a brand
   only ever needs to happen in one place. */
(function () {
  'use strict';
  window.BlackArrow3DBrands = [
    'Bambu Lab',
    'Creality',
    'Elegoo',
    'Flashforge',
    'Anycubic',
    'Snapmaker',
    'Polymaker',
    'eSUN',
    'Sunlu',
    'Generic',
    'Black Arrow'
  ];
})();
