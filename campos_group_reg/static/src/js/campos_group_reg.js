odoo.define('campos_group_reg.campos_group_reg', function (require) {
"use strict";

require('web.dom_ready');

  /**
  * Show/hide manual name/address fields
  */
  function toggle_manual_fields() {
	var req = true
	if ($("#same_as_contact").is(":checked")) {
		req = false
    $("#treasurer_mobile").prop('required', req);
    //$("#treasurer_mobile").prop('disabled', req)
    $("#treasurer_email").prop('required', req);
    //$("#treasurer_email").prop('disabled', req)
    //$("treasurer_email").toggle(req);
  }
  
  console.debug("[CAMPOS] Group Reg JS is loading...");

  // Bind manual name/address fields funtion to select element
  $("#same_as_contact").change(toggle_manual_fields);
  //- and run initial check
  toggle_manual_fields();
    
  

  

});