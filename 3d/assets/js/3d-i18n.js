/* Black Arrow 3D — EN/AR language switch.
   Static chrome (nav, footer, section headers, forms) is translated via
   [data-i18n] text replacement. Dynamic content rendered by 3d-store.js
   (product cards/detail, cart, compare) calls BlackArrow3DI18n.t(key)
   directly, and uses a product's *_ar fields when the language is Arabic
   and that field exists (falls back to English otherwise — nothing
   breaks for a product that hasn't been translated yet). */
(function () {
  'use strict';

  var LANG_KEY = 'b3d_lang_v1';

  var DICT = {
    en: {
      nav_shop: 'Shop',
      nav_3d_printers: '3D Printers',
      nav_filaments: 'Filaments',
      nav_accessories: 'Accessories',
      nav_brands: 'Brands',
      nav_all_brands: 'All Brands',
      nav_profile: 'Profile',
      nav_bag: 'Bag',
      nav_tagline: 'Printing Equipment & Supplies',
      nav_black_arrow_3d_full: 'Black Arrow 3D',

      footer_home: 'Home',
      footer_cart: 'Cart',
      footer_compare: 'Compare',
      footer_my_account: 'My Account',
      footer_col_venture: 'Black Arrow Venture',
      footer_main_site: 'Main Site',
      footer_services: 'Services',
      footer_contact: 'Contact',
      footer_brand_desc: 'A Black Arrow Venture company line of business. 3D printing equipment & supplies.',
      footer_copyright: 'Black Arrow Venture company. All rights reserved.',
      footer_privacy: 'Privacy Policy',
      footer_terms: 'Terms of Service',

      hub_preview_banner: 'Preview — not yet open for orders',
      hub_hero_eyebrow: 'Additive Manufacturing',
      hub_hero_h1_a: '3D Printers & Materials,',
      hub_hero_h1_b: 'the Black Arrow Way',
      hub_hero_p: 'Desktop and industrial FDM printers, resin systems, and print materials — sourced, specified, and supported with the same reliability standard as our critical infrastructure work.',
      hub_explore_shop: 'Explore the Shop',
      hub_ask_question: 'Ask a Question',
      hub_cat1_title: 'FDM Printers',
      hub_cat1_desc: 'Desktop to industrial scale',
      hub_cat2_title: 'Resin (SLA/MSLA)',
      hub_cat2_desc: 'High-detail printing',
      hub_cat3_desc: 'PLA, PETG, ABS & more',
      hub_cat4_title: 'Resins & Accessories',
      hub_cat4_desc: 'Everything to keep printing',
      hub_why_overline: 'Why Black Arrow 3D',
      hub_why_h2: 'Sourced and Supported Like Everything Else We Sell',
      hub_why_li1: 'Equipment selected for reliability, not just spec-sheet numbers',
      hub_why_li2: 'Genuine spare parts and consumables kept available, not one-time drop-shipped',
      hub_why_li3: 'Support from a team that already handles critical infrastructure equipment',
      hub_cta_h2: 'Ready to Browse the Catalog?',
      hub_cta_p: 'Catalog is being set up — check back soon',

      b3d_shop_eyebrow: 'Black Arrow 3D Catalog',
      b3d_shop_h1_a: 'Build smarter.',
      b3d_shop_h1_b: 'Print without limits.',
      b3d_shop_p: 'Equipment, materials and workshop support selected for makers, educators and production teams.',
      b3d_shop_products: 'Shop products',
      b3d_compare_printers: 'Compare printers',

      shop_by_brand_overline: 'Shop by Brand',
      shop_choose_manufacturer: 'Choose a manufacturer',
      shop_choose_manufacturer_desc: 'Select one brand to view its available printers, filaments and compatible accessories.',
      shop_brand_label: 'Brand',
      shop_all_brands: 'All brands',
      shop_catalog_banner: "We're setting up the catalog now — products are being added.",
      shop_all: 'All',
      shop_search_placeholder: 'Search products',
      shop_filters_btn: 'Filters',
      shop_featured: 'Featured',
      shop_instock: 'In stock',
      shop_pricerange: 'Price range',
      shop_topquality: 'Top quality',
      shop_products_published: 'products published',
      shop_sort_featured: 'Sort: Featured',
      shop_sort_price_asc: 'Price: Low to High',
      shop_sort_price_desc: 'Price: High to Low',
      shop_sort_name_asc: 'Name: A–Z',

      filter_avail_legend: 'Availability',
      filter_instock_only: 'In stock only',
      filter_preorder_only: 'Pre-order only',
      filter_highlights_legend: 'Highlights',
      filter_onsale: 'On sale',
      filter_pricerange_legend: 'Price range (SAR)',
      filter_min: 'Min',
      filter_max: 'Max',

      pd_crumb_default: 'Product',
      pd_loading: 'Loading product…',

      cart_overline: 'Your Selection',
      cart_h1: 'Shopping Cart',
      cart_empty_h2: 'Your cart is empty',
      cart_empty_p: 'Browse the catalog and add a product to get started.',
      cart_go_shop: 'Go to Shop',
      cart_summary_h3: 'Order Summary',
      cart_subtotal: 'Subtotal',
      cart_shipping_label: 'Shipping',
      cart_shipping_value: 'Calculated at checkout',
      cart_total_label: 'Total',
      cart_payment_h4: 'Payment Method',
      cart_checkout_note: "Online payment (mada / cards / Apple Pay / STC Pay) is pending our Moyasar merchant approval — it will be enabled here the moment it's live. Bank transfer and quotation requests already work via our contact form.",

      pm_pending: 'Pending approval',
      pm_notenabled: 'Not yet enabled',
      pm_cod: 'Cash on Delivery',
      pm_banktransfer: 'Bank Transfer',
      pm_quotation: 'Business Quotation',
      pm_bank_h4: 'Direct Bank Transfer',
      pm_bank_p: "Transfer the order total to Black Arrow Venture's account and send us the reference — we'll confirm once verified. Bank details will be added here once approved.",
      pm_bank_order_number: 'Order Number',
      pm_bank_beneficiary: 'Beneficiary Name',
      pm_bank_bankname: 'Bank Name',
      pm_bank_iban: 'IBAN',
      pm_bank_request_btn: 'Request Bank Details',
      pm_quote_h4: 'Business Quotation / Invoice',
      pm_quote_p: "Prefer a formal quotation or invoice for procurement? Send us your cart and we'll prepare one.",
      pm_quote_request_btn: 'Request a Quotation',

      account_overline: 'Customer Account',
      account_notconfigured: "Sign-in isn't connected yet — we're setting up a free Black Arrow 3D account system. This page will let you sign in with email once that's ready.",
      account_signin_tab: 'Sign In',
      account_signup_tab: 'Create Account',
      account_email: 'Email',
      account_password: 'Password',
      account_password_min: 'Password (min. 6 characters)',
      account_agree_1: 'By continuing you agree to our',
      account_agree_and: 'and',
      account_google_apple_note: 'Google and Apple sign-in are not enabled yet — email sign-in only, for now.',
      account_signed_in_as: 'Signed in as',
      account_signout: 'Sign Out',
      account_saved_products: 'Saved Products',
      account_saved_products_empty: 'Nothing saved yet — use the ♡ icon on a product to save it here.',
      account_order_history: 'Order History',
      account_order_history_empty: 'No orders yet.',
      account_order_tracking: 'Order Tracking',
      account_order_tracking_empty: 'Nothing to track yet.',
      account_addresses: 'Addresses',
      account_addresses_empty: 'No saved addresses yet.',
      account_comm_prefs: 'Communication Preferences',
      account_comm_prefs_desc: 'Default: order updates only. Marketing emails are off unless you opt in later.',

      compare_overline: 'Side by Side',
      compare_h1: 'Compare Products',

      js_add_to_cart: 'Add to Cart',
      js_out_of_stock: 'Out of Stock',
      js_pre_order: 'Pre-Order',
      js_view_options: 'View Options',
      js_from: 'From',
      js_added: 'Added ✓',
      js_compare_btn: 'Compare',
      js_added_to_compare: 'Added to Compare',
      js_view_cart: 'View Cart',
      js_remove: 'Remove',
      js_no_products_published: 'No products published yet',
      js_check_back_soon: 'Check back soon, or contact us for current availability.',
      js_related_products: 'Related Products',
      js_product_not_found: 'Product not found',
      js_product_not_found_desc: 'That product isn’t in the catalog yet.',
      js_back_to_shop: 'Back to shop',
      js_shipping_heading: 'Shipping',
      js_shipping_desc: 'Calculated at checkout, across Saudi Arabia.',
      js_returns_heading: 'Returns',
      js_returns_desc_prefix: 'See our',
      js_returns_desc_suffix: 'for the return policy.',
      js_compatibility_heading: 'Compatibility',
      js_warranty_heading: 'Warranty',
      js_nothing_to_compare_h2: 'Nothing to compare yet',
      js_nothing_to_compare_p: 'Add at least two published products to your comparison list from the shop — none published yet.',
      js_cmp_price: 'Price',
      js_cmp_quality: 'Print quality',
      js_cmp_speed: 'Printing speed',
      js_cmp_buildvolume: 'Build volume',
      js_cmp_material: 'Material capability',
      js_cmp_easeofuse: 'Ease of use',
      js_cmp_experience: 'Experience level',
      js_cmp_warranty: 'Warranty & support',
      js_cmp_usecase: 'Best use case',
      js_cmp_accessories: 'Accessories & compatibility',
      js_motion_on: 'Motion: On',
      js_motion_off: 'Motion: Off',
      js_product_image: 'Product image',
      js_sale_badge: 'Sale',
      announce_1: 'Black Arrow 3D preview — catalog is being set up, check back soon.',
      announce_2: 'Business quotations available now — contact us for a project quote.',
      announce_3: 'Online payment is pending gateway approval — accounts and browsing are open.'
    },
    ar: {
      nav_shop: 'المتجر',
      nav_3d_printers: 'طابعات ثلاثية الأبعاد',
      nav_filaments: 'خيوط الطباعة',
      nav_accessories: 'الملحقات',
      nav_brands: 'العلامات التجارية',
      nav_all_brands: 'جميع العلامات التجارية',
      nav_profile: 'الحساب',
      nav_bag: 'السلة',
      nav_tagline: 'معدات وتوريدات الطباعة ثلاثية الأبعاد',
      nav_black_arrow_3d_full: 'بلاك أرو 3D',

      footer_home: 'الرئيسية',
      footer_cart: 'عربة التسوق',
      footer_compare: 'مقارنة',
      footer_my_account: 'حسابي',
      footer_col_venture: 'بلاك أرو فنتشر',
      footer_main_site: 'الموقع الرئيسي',
      footer_services: 'الخدمات',
      footer_contact: 'اتصل بنا',
      footer_brand_desc: 'أحد قطاعات أعمال شركة بلاك أرو فنتشر. معدات وتوريدات الطباعة ثلاثية الأبعاد.',
      footer_copyright: 'شركة بلاك أرو فنتشر. جميع الحقوق محفوظة.',
      footer_privacy: 'سياسة الخصوصية',
      footer_terms: 'شروط الخدمة',

      hub_preview_banner: 'معاينة — لم يُفتح بعد لاستقبال الطلبات',
      hub_hero_eyebrow: 'التصنيع الإضافي',
      hub_hero_h1_a: 'طابعات ومواد ثلاثية الأبعاد،',
      hub_hero_h1_b: 'على طريقة بلاك أرو',
      hub_hero_p: 'طابعات FDM للاستخدام المكتبي والصناعي، وأنظمة الراتنج، ومواد الطباعة — يتم اختيارها وتوريدها ودعمها بنفس معايير الموثوقية المعتمدة في أعمالنا للبنية التحتية الحرجة.',
      hub_explore_shop: 'استكشف المتجر',
      hub_ask_question: 'اطرح سؤالاً',
      hub_cat1_title: 'طابعات FDM',
      hub_cat1_desc: 'من الحجم المكتبي إلى الصناعي',
      hub_cat2_title: 'الراتنج (SLA/MSLA)',
      hub_cat2_desc: 'طباعة عالية الدقة',
      hub_cat3_desc: 'PLA وPETG وABS وغيرها',
      hub_cat4_title: 'الراتنج والملحقات',
      hub_cat4_desc: 'كل ما يلزم لمواصلة الطباعة',
      hub_why_overline: 'لماذا بلاك أرو 3D',
      hub_why_h2: 'مورَّدة ومدعومة بنفس معايير كل ما نبيعه',
      hub_why_li1: 'معدات تُختار لموثوقيتها، لا لمجرد أرقام في نشرة المواصفات',
      hub_why_li2: 'قطع غيار ومستهلكات أصلية متوفرة باستمرار، وليست بنظام الشحن المباشر لمرة واحدة',
      hub_why_li3: 'دعم من فريق يتولى بالفعل معدات البنية التحتية الحرجة',
      hub_cta_h2: 'هل أنت مستعد لتصفح الكتالوج؟',
      hub_cta_p: 'جارٍ إعداد الكتالوج — تابعونا قريباً',

      b3d_shop_eyebrow: 'كتالوج بلاك أرو 3D',
      b3d_shop_h1_a: 'اطبع بذكاء.',
      b3d_shop_h1_b: 'بلا حدود.',
      b3d_shop_p: 'معدات ومواد ودعم ورشة عمل، مُختارة لصنّاع المحتوى والمعلّمين وفرق الإنتاج.',
      b3d_shop_products: 'تسوّق المنتجات',
      b3d_compare_printers: 'قارن بين الطابعات',

      shop_by_brand_overline: 'تسوّق حسب العلامة التجارية',
      shop_choose_manufacturer: 'اختر الشركة المصنّعة',
      shop_choose_manufacturer_desc: 'اختر علامة تجارية واحدة لعرض طابعاتها وخيوطها وملحقاتها المتوافقة.',
      shop_brand_label: 'العلامة التجارية',
      shop_all_brands: 'جميع العلامات التجارية',
      shop_catalog_banner: 'جارٍ إعداد الكتالوج الآن — يتم إضافة المنتجات.',
      shop_all: 'الكل',
      shop_search_placeholder: 'ابحث عن المنتجات',
      shop_filters_btn: 'التصفية',
      shop_featured: 'مميز',
      shop_instock: 'متوفر',
      shop_pricerange: 'نطاق السعر',
      shop_topquality: 'الأعلى جودة',
      shop_products_published: 'منتج منشور',
      shop_sort_featured: 'الترتيب: المميز',
      shop_sort_price_asc: 'السعر: من الأقل إلى الأعلى',
      shop_sort_price_desc: 'السعر: من الأعلى إلى الأقل',
      shop_sort_name_asc: 'الاسم: أ-ي',

      filter_avail_legend: 'التوفر',
      filter_instock_only: 'المتوفر فقط',
      filter_preorder_only: 'الطلب المسبق فقط',
      filter_highlights_legend: 'أبرز الميزات',
      filter_onsale: 'عليه تخفيض',
      filter_pricerange_legend: 'نطاق السعر (ريال سعودي)',
      filter_min: 'الأدنى',
      filter_max: 'الأقصى',

      pd_crumb_default: 'المنتج',
      pd_loading: 'جارٍ تحميل المنتج…',

      cart_overline: 'اختيارك',
      cart_h1: 'عربة التسوق',
      cart_empty_h2: 'عربة التسوق فارغة',
      cart_empty_p: 'تصفّح الكتالوج وأضف منتجاً للبدء.',
      cart_go_shop: 'الذهاب إلى المتجر',
      cart_summary_h3: 'ملخص الطلب',
      cart_subtotal: 'المجموع الفرعي',
      cart_shipping_label: 'الشحن',
      cart_shipping_value: 'يُحتسب عند إتمام الطلب',
      cart_total_label: 'الإجمالي',
      cart_payment_h4: 'طريقة الدفع',
      cart_checkout_note: 'الدفع الإلكتروني (مدى / البطاقات / Apple Pay / STC Pay) بانتظار اعتماد بوابة الدفع لدينا — سيتم تفعيله هنا فور جاهزيته. طلبات التحويل البنكي وعروض الأسعار متاحة بالفعل عبر نموذج التواصل.',

      pm_pending: 'بانتظار الاعتماد',
      pm_notenabled: 'غير مُفعّل بعد',
      pm_cod: 'الدفع عند الاستلام',
      pm_banktransfer: 'تحويل بنكي',
      pm_quotation: 'طلب عرض سعر',
      pm_bank_h4: 'التحويل البنكي المباشر',
      pm_bank_p: 'حوّل إجمالي الطلب إلى حساب بلاك أرو فنتشر وأرسل لنا رقم المرجع — سنؤكد الطلب بعد التحقق. سيتم إضافة بيانات الحساب البنكي هنا بعد اعتمادها.',
      pm_bank_order_number: 'رقم الطلب',
      pm_bank_beneficiary: 'اسم المستفيد',
      pm_bank_bankname: 'اسم البنك',
      pm_bank_iban: 'رقم الآيبان (IBAN)',
      pm_bank_request_btn: 'طلب بيانات الحساب البنكي',
      pm_quote_h4: 'طلب عرض سعر / فاتورة للأعمال',
      pm_quote_p: 'هل تفضّل عرض سعر أو فاتورة رسمية للمشتريات؟ أرسل لنا محتوى عربتك وسنجهزها لك.',
      pm_quote_request_btn: 'طلب عرض سعر',

      account_overline: 'حساب العميل',
      account_notconfigured: 'تسجيل الدخول غير مُفعّل بعد — نعمل على إعداد نظام حسابات مجاني لبلاك أرو 3D. ستتمكن من تسجيل الدخول بالبريد الإلكتروني بمجرد جاهزيته.',
      account_signin_tab: 'تسجيل الدخول',
      account_signup_tab: 'إنشاء حساب',
      account_email: 'البريد الإلكتروني',
      account_password: 'كلمة المرور',
      account_password_min: 'كلمة المرور (٦ أحرف على الأقل)',
      account_agree_1: 'بالمتابعة، فإنك توافق على',
      account_agree_and: 'و',
      account_google_apple_note: 'تسجيل الدخول عبر Google وApple غير مُفعّل بعد — التسجيل بالبريد الإلكتروني فقط حالياً.',
      account_signed_in_as: 'تم تسجيل الدخول باسم',
      account_signout: 'تسجيل الخروج',
      account_saved_products: 'المنتجات المحفوظة',
      account_saved_products_empty: 'لا توجد منتجات محفوظة بعد — استخدم أيقونة ♡ على أي منتج لحفظه هنا.',
      account_order_history: 'سجل الطلبات',
      account_order_history_empty: 'لا توجد طلبات بعد.',
      account_order_tracking: 'تتبّع الطلب',
      account_order_tracking_empty: 'لا يوجد ما يمكن تتبعه بعد.',
      account_addresses: 'العناوين',
      account_addresses_empty: 'لا توجد عناوين محفوظة بعد.',
      account_comm_prefs: 'تفضيلات التواصل',
      account_comm_prefs_desc: 'الافتراضي: تحديثات الطلبات فقط. رسائل التسويق مُعطّلة ما لم تُفعّلها لاحقاً.',

      compare_overline: 'جنباً إلى جنب',
      compare_h1: 'مقارنة المنتجات',

      js_add_to_cart: 'أضف إلى السلة',
      js_out_of_stock: 'غير متوفر',
      js_pre_order: 'طلب مسبق',
      js_view_options: 'عرض الخيارات',
      js_from: 'يبدأ من',
      js_added: 'أُضيف ✓',
      js_compare_btn: 'قارن',
      js_added_to_compare: 'أُضيف للمقارنة',
      js_view_cart: 'عرض السلة',
      js_remove: 'إزالة',
      js_no_products_published: 'لا توجد منتجات منشورة بعد',
      js_check_back_soon: 'تابعونا قريباً، أو تواصلوا معنا لمعرفة التوفر الحالي.',
      js_related_products: 'منتجات ذات صلة',
      js_product_not_found: 'المنتج غير موجود',
      js_product_not_found_desc: 'هذا المنتج غير متوفر في الكتالوج بعد.',
      js_back_to_shop: 'العودة إلى المتجر',
      js_shipping_heading: 'الشحن',
      js_shipping_desc: 'يُحتسب عند إتمام الطلب، لجميع مناطق المملكة العربية السعودية.',
      js_returns_heading: 'الإرجاع',
      js_returns_desc_prefix: 'راجع',
      js_returns_desc_suffix: 'لمعرفة سياسة الإرجاع.',
      js_compatibility_heading: 'التوافق',
      js_warranty_heading: 'الضمان',
      js_nothing_to_compare_h2: 'لا يوجد ما يمكن مقارنته بعد',
      js_nothing_to_compare_p: 'أضف منتجين منشورين على الأقل إلى قائمة المقارنة من المتجر — لا توجد منتجات منشورة بعد.',
      js_cmp_price: 'السعر',
      js_cmp_quality: 'جودة الطباعة',
      js_cmp_speed: 'سرعة الطباعة',
      js_cmp_buildvolume: 'حجم الطباعة',
      js_cmp_material: 'التوافق مع المواد',
      js_cmp_easeofuse: 'سهولة الاستخدام',
      js_cmp_experience: 'مستوى الخبرة',
      js_cmp_warranty: 'الضمان والدعم',
      js_cmp_usecase: 'أفضل استخدام',
      js_cmp_accessories: 'الملحقات والتوافق',
      js_motion_on: 'الحركة: تشغيل',
      js_motion_off: 'الحركة: إيقاف',
      js_product_image: 'صورة المنتج',
      js_sale_badge: 'خصم',
      announce_1: 'معاينة بلاك أرو 3D — جارٍ إعداد الكتالوج، تابعونا قريباً.',
      announce_2: 'عروض الأسعار للأعمال متاحة الآن — تواصل معنا لطلب عرض سعر لمشروعك.',
      announce_3: 'الدفع الإلكتروني بانتظار اعتماد بوابة الدفع — التصفح وإنشاء الحسابات متاحان.'
    }
  };

  function getLang() {
    try {
      return localStorage.getItem(LANG_KEY) === 'ar' ? 'ar' : 'en';
    } catch (e) { return 'en'; }
  }

  function setLang(lang) {
    try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
  }

  function t(key) {
    var lang = getLang();
    if (DICT[lang] && DICT[lang][key] != null) return DICT[lang][key];
    if (DICT.en[key] != null) return DICT.en[key];
    return key;
  }

  function applyDirection(lang) {
    document.documentElement.setAttribute('lang', lang === 'ar' ? 'ar' : 'en');
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
  }

  function translateStaticPage() {
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      var val = t(key);
      if (val != null) el.textContent = val;
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
      el.setAttribute('placeholder', t(el.getAttribute('data-i18n-placeholder')));
    });
    document.querySelectorAll('[data-i18n-motion]').forEach(function (el) {
      var pressed = el.closest('[aria-pressed]');
      var isOff = pressed && pressed.getAttribute('aria-pressed') === 'true';
      el.textContent = isOff ? t('js_motion_off') : t('js_motion_on');
    });
  }

  function initLangToggle() {
    var lang = getLang();
    applyDirection(lang);
    translateStaticPage();
    document.querySelectorAll('[data-lang-toggle]').forEach(function (btn) {
      btn.textContent = lang === 'ar' ? 'EN' : 'AR';
      btn.addEventListener('click', function () {
        setLang(lang === 'ar' ? 'en' : 'ar');
        location.reload();
      });
    });
  }

  window.BlackArrow3DI18n = {
    getLang: getLang,
    setLang: setLang,
    t: t,
    applyDirection: applyDirection,
    translateStaticPage: translateStaticPage
  };

  applyDirection(getLang());
  document.addEventListener('DOMContentLoaded', initLangToggle);
})();
