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
      nav_blog: 'Blog',
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
      footer_whatsapp: 'WhatsApp',
      footer_address: 'Dammam, Eastern Province, Saudi Arabia',
      footer_cr_vat: 'CR 7054542985 · VAT 314841084500003',
      footer_brand_desc: 'A Black Arrow Venture company line of business. 3D printing equipment & supplies.',
      footer_copyright: 'Black Arrow Venture company. All rights reserved.',
      footer_privacy: 'Privacy Policy',
      footer_terms: 'Terms of Service',

      hub_preview_banner: 'Now Live — Shop 3D Printers, Filament & Accessories',
      hub_hero_eyebrow: '3D Printing, Made Easy',
      hub_hero_h1_a: 'The 3D Printer That',
      hub_hero_h1_b: 'Fits Your Project',
      hub_hero_p: 'Bambu Lab, Creality, Elegoo, Snapmaker, Anycubic and Flashforge printers, filament and accessories — for makers, students, schools and home users across Saudi Arabia. Genuine warranty, real support, and delivery to your door in Riyadh, Jeddah, Dammam and beyond.',
      hub_explore_shop: 'Shop 3D Printers',
      hub_ask_question: 'Not Sure Which One? Ask Us',
      hub_cat1_title: 'FDM Printers',
      hub_cat1_desc: 'Desktop to industrial scale',
      hub_cat2_title: 'Resin (SLA/MSLA)',
      hub_cat2_desc: 'High-detail printing',
      hub_cat3_desc: 'PLA, PETG, ABS & more',
      hub_cat4_title: 'Resins & Accessories',
      hub_cat4_desc: 'Everything to keep printing',
      hub_why_overline: 'Why Buy From Black Arrow 3D',
      hub_why_h2: 'Real Printers, Real Support, Real Warranty',
      hub_why_li1: 'Printers picked for everyday reliability, not just spec-sheet numbers',
      hub_why_li2: 'Genuine spare parts and consumables kept in stock — not a one-time drop-ship',
      hub_why_li3: 'Setup help and after-sales support from a real local team, in Arabic or English',
      hub_cta_h2: 'Ready to Browse the Catalog?',
      hub_cta_p: 'Browse 3D printers, filament and accessories from Bambu Lab, Creality, Elegoo, Snapmaker, Anycubic and Flashforge.',

      b3d_shop_eyebrow: 'Black Arrow 3D Catalog',
      b3d_shop_h1_a: 'Build smarter.',
      b3d_shop_h1_b: 'Print without limits.',
      b3d_shop_h1_page: 'Shop',
      b3d_shop_p: 'Equipment, materials and workshop support selected for makers, educators and production teams across Saudi Arabia — priced in SAR with nationwide delivery.',
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
      filter_brand_legend: 'Brand',
      filter_printertype_legend: 'Printer type',
      filter_buildvolume_legend: 'Build volume',
      filter_filamentmaterial_legend: 'Filament material',
      filter_accessorycompat_legend: 'Accessory compatibility',
      filter_all_option: 'All',
      filter_bv_compact: 'Compact (under 220 mm)',
      filter_bv_standard: 'Standard (220–300 mm)',
      filter_bv_large: 'Large (300 mm+)',
      filter_apply: 'Apply Filters',
      filter_clear: 'Clear all',
      js_from_tooltip: 'Starting price — final price depends on the option you choose (e.g. Standalone vs Combo).',
      trust_delivery: 'Delivery across Saudi Arabia',
      trust_payment: 'Secure payment',
      trust_vat: 'VAT invoice',
      trust_warranty: 'Manufacturer warranty',
      trust_quotation: 'Business quotations',
      trust_support: 'Local support',
      js_card_delivery: 'Delivery: KSA-wide',
      js_card_warranty: 'Warranty included',

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
      cart_checkout_note: 'Cash on Delivery and Bank Transfer are available now. Card payments (mada / Visa / Mastercard / Apple Pay / STC Pay) are coming soon, pending our payment gateway approval.',

      pm_soon: 'Coming Soon',
      pm_cod: 'Cash on Delivery',
      pm_banktransfer: 'Bank Transfer',
      pm_quotation: 'Business Quotation',
      pm_bank_h4: 'Direct Bank Transfer',
      pm_bank_p: "Transfer the order total to the account below, then complete the form and attach your transfer reference in the notes — we'll confirm once it's received.",
      pm_bank_bankname: 'Bank Name',
      pm_bank_beneficiary: 'Beneficiary Name',
      pm_bank_iban: 'IBAN',
      pm_bank_iban_note: 'IBAN is all you need for a domestic transfer within Saudi Arabia.',
      pm_quote_h4: 'Business Quotation / Invoice',
      pm_quote_p: "Prefer a formal quotation or invoice for procurement? Send us your cart and we'll prepare one.",
      pm_quote_request_btn: 'Request a Quotation',

      checkout_h4: 'Delivery Details',
      checkout_name: 'Full Name',
      checkout_phone: 'Phone',
      checkout_city: 'City',
      checkout_address: 'Full Address',
      checkout_notes: 'Notes (optional)',
      checkout_submit: 'Place Order',
      checkout_success: "Order received — we'll contact you shortly to confirm.",
      checkout_error: 'Sorry, the order could not be sent. Please WhatsApp us instead.',

      account_overline: 'Customer Account',
      account_notconfigured: "Sign-in isn't connected yet — we're setting up a free Black Arrow 3D account system. This page will let you sign in with email once that's ready.",
      account_signin_tab: 'Sign In',
      account_signup_tab: 'Create Account',
      account_name: 'Full name',
      account_phone: 'Phone',
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
      announce_1: 'Black Arrow 3D — shop 3D printers, filament and accessories, delivered across Saudi Arabia.',
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
      nav_blog: 'المدونة',
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
      footer_whatsapp: 'واتساب',
      footer_address: 'الدمام، المنطقة الشرقية، المملكة العربية السعودية',
      footer_cr_vat: 'سجل تجاري 7054542985 · الرقم الضريبي 314841084500003',
      footer_brand_desc: 'أحد قطاعات أعمال شركة بلاك أرو فنتشر. معدات وتوريدات الطباعة ثلاثية الأبعاد.',
      footer_copyright: 'شركة بلاك أرو فنتشر. جميع الحقوق محفوظة.',
      footer_privacy: 'سياسة الخصوصية',
      footer_terms: 'شروط الخدمة',

      hub_preview_banner: 'متاح الآن — تسوّق الطابعات ثلاثية الأبعاد والفلمنت والملحقات',
      hub_hero_eyebrow: 'الطباعة ثلاثية الأبعاد، ببساطة',
      hub_hero_h1_a: 'الطابعة ثلاثية الأبعاد',
      hub_hero_h1_b: 'المناسبة لمشروعك',
      hub_hero_p: 'طابعات وفلامنت وملحقات Bambu Lab وCreality وElegoo وSnapmaker وAnycubic وFlashforge — لصناع المحتوى والطلاب والمدارس والاستخدام المنزلي في جميع أنحاء المملكة. ضمان أصلي، ودعم حقيقي، وتوصيل لباب المنزل في الرياض وجدة والدمام وغيرها.',
      hub_explore_shop: 'تسوّق الطابعات ثلاثية الأبعاد',
      hub_ask_question: 'غير متأكد أيها تختار؟ اسألنا',
      hub_cat1_title: 'طابعات FDM',
      hub_cat1_desc: 'من الحجم المكتبي إلى الصناعي',
      hub_cat2_title: 'الراتنج (SLA/MSLA)',
      hub_cat2_desc: 'طباعة عالية الدقة',
      hub_cat3_desc: 'PLA وPETG وABS وغيرها',
      hub_cat4_title: 'الراتنج والملحقات',
      hub_cat4_desc: 'كل ما يلزم لمواصلة الطباعة',
      hub_why_overline: 'لماذا تشتري من بلاك أرو 3D',
      hub_why_h2: 'طابعات حقيقية، ودعم حقيقي، وضمان حقيقي',
      hub_why_li1: 'طابعات تُختار لموثوقيتها في الاستخدام اليومي، لا لمجرد أرقام في نشرة المواصفات',
      hub_why_li2: 'قطع غيار ومستهلكات أصلية متوفرة باستمرار، وليست بنظام الشحن المباشر لمرة واحدة',
      hub_why_li3: 'مساعدة في التركيب ودعم ما بعد البيع من فريق محلي حقيقي، بالعربية أو الإنجليزية',
      hub_cta_h2: 'هل أنت مستعد لتصفح الكتالوج؟',
      hub_cta_p: 'تصفح الطابعات ثلاثية الأبعاد والفلمنت والملحقات من Bambu Lab وCreality وElegoo وSnapmaker وAnycubic وFlashforge.',

      b3d_shop_eyebrow: 'كتالوج بلاك أرو 3D',
      b3d_shop_h1_a: 'اطبع بذكاء.',
      b3d_shop_h1_b: 'بلا حدود.',
      b3d_shop_h1_page: 'المتجر',
      b3d_shop_p: 'معدات ومواد ودعم ورشة عمل، مُختارة لصنّاع المحتوى والمعلّمين وفرق الإنتاج في جميع أنحاء المملكة العربية السعودية — أسعار بالريال السعودي مع توصيل لكل المناطق.',
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
      filter_brand_legend: 'العلامة التجارية',
      filter_printertype_legend: 'نوع الطابعة',
      filter_buildvolume_legend: 'حجم الطباعة',
      filter_filamentmaterial_legend: 'خامة الفلمنت',
      filter_accessorycompat_legend: 'التوافق مع الطابعات',
      filter_all_option: 'الكل',
      filter_bv_compact: 'صغير (أقل من 220 مم)',
      filter_bv_standard: 'متوسط (220–300 مم)',
      filter_bv_large: 'كبير (300 مم فأكثر)',
      filter_apply: 'تطبيق الفلاتر',
      filter_clear: 'مسح الكل',
      js_from_tooltip: 'السعر الابتدائي — السعر النهائي يعتمد على الخيار الذي تختاره (مثلاً منفردة أو باقة).',
      trust_delivery: 'توصيل لجميع مناطق السعودية',
      trust_payment: 'دفع آمن',
      trust_vat: 'فاتورة ضريبية',
      trust_warranty: 'ضمان الشركة المصنّعة',
      trust_quotation: 'عروض أسعار للأعمال',
      trust_support: 'دعم محلي',
      js_card_delivery: 'توصيل لكل المملكة',
      js_card_warranty: 'يشمل الضمان',

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
      cart_checkout_note: 'الدفع عند الاستلام والتحويل البنكي متاحان الآن. الدفع بالبطاقة (مدى / فيزا / ماستركارد / Apple Pay / STC Pay) قريباً، بانتظار اعتماد بوابة الدفع لدينا.',

      pm_soon: 'قريباً',
      pm_cod: 'الدفع عند الاستلام',
      pm_banktransfer: 'تحويل بنكي',
      pm_quotation: 'طلب عرض سعر',
      pm_bank_h4: 'التحويل البنكي المباشر',
      pm_bank_p: 'حوّل إجمالي الطلب إلى الحساب أدناه، ثم أكمل النموذج وأضف رقم مرجع التحويل في الملاحظات — سنؤكد الطلب فور استلامه.',
      pm_bank_bankname: 'اسم البنك',
      pm_bank_beneficiary: 'اسم المستفيد',
      pm_bank_iban: 'رقم الآيبان (IBAN)',
      pm_bank_iban_note: 'رقم الآيبان وحده كافٍ لإتمام التحويل داخل المملكة العربية السعودية.',
      pm_quote_h4: 'طلب عرض سعر / فاتورة للأعمال',
      pm_quote_p: 'هل تفضّل عرض سعر أو فاتورة رسمية للمشتريات؟ أرسل لنا محتوى عربتك وسنجهزها لك.',
      pm_quote_request_btn: 'طلب عرض سعر',

      checkout_h4: 'تفاصيل التوصيل',
      checkout_name: 'الاسم الكامل',
      checkout_phone: 'رقم الجوال',
      checkout_city: 'المدينة',
      checkout_address: 'العنوان الكامل',
      checkout_notes: 'ملاحظات (اختياري)',
      checkout_submit: 'تأكيد الطلب',
      checkout_success: 'تم استلام طلبك — سنتواصل معك قريباً للتأكيد.',
      checkout_error: 'عذراً، تعذّر إرسال الطلب. يرجى التواصل معنا عبر واتساب.',

      account_overline: 'حساب العميل',
      account_notconfigured: 'تسجيل الدخول غير مُفعّل بعد — نعمل على إعداد نظام حسابات مجاني لبلاك أرو 3D. ستتمكن من تسجيل الدخول بالبريد الإلكتروني بمجرد جاهزيته.',
      account_signin_tab: 'تسجيل الدخول',
      account_signup_tab: 'إنشاء حساب',
      account_name: 'الاسم الكامل',
      account_phone: 'رقم الجوال',
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
      announce_1: 'بلاك أرو 3D — تسوّق الطابعات ثلاثية الأبعاد والفلمنت والملحقات، مع التوصيل داخل السعودية.',
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
