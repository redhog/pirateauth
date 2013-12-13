import openid_provider.utils

def get_sreg_data(request, orequest):
    res = dict(openid_provider.utils.get_default_sreg_data(request, orequest))

    return res

def get_ax_data(request, orequest):
    res = dict(openid_provider.utils.get_default_ax_data(request, orequest))

#    import pdb
#    pdb.set_trace()

    return res
