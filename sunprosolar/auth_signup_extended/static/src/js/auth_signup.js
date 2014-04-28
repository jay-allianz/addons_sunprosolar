openerp.auth_signup_extended = function(instance){
    instance.auth_signup = instance.auth_signup || {};
    var _t = instance.web._t;
    instance.web.Login.include({
        start: function() {
            var self = this;
            return this._super().always(function() {
                // Switches the login box to the select mode whith mode == [default|signup|reset]
                	console.log("HERERERRERERE",self)
                    var mode = self.get('login_mode') || 'default';
                    self.$('*[data-modes]').each(function() {
                        var modes = $(this).data('modes').split(/\s+/);
                        $(this).toggle(modes.indexOf(mode) > -1);
                    });
                    self.$('a.oe_signup_signup').hide()
                    self.$('a.oe_signup_reset_password').hide()
//                    self.$('a.oe_signup_reset_password').toggle(self.reset_password_enabled);
                });
            });
        },
    })
}