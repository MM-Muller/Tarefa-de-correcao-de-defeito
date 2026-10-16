"""Processamento de pedidos."""


def inteiro(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def processar_pedido(itens, estoque, desconto_percentual=0):
    """Retorna subtotal, desconto, frete e total, todos em centavos."""
    if not isinstance(itens, list) or not itens or not isinstance(estoque, dict):
        raise ValueError('Pedido ou estoque inválido')
    if not inteiro(desconto_percentual) or not 0 <= desconto_percentual <= 30:
        raise ValueError('Desconto inválido')
    for disponivel in estoque.values():
        if not inteiro(disponivel) or disponivel < 0:
            raise ValueError('Estoque inválido')

    subtotal = 0
    solicitados = {}
    for item in itens:
        if not isinstance(item, dict):
            raise ValueError('Item inválido')
        sku = item.get('sku')
        preco = item.get('preco_centavos')
        quantidade = item.get('quantidade')
        if not isinstance(sku, str) or not sku.strip() or sku not in estoque:
            raise ValueError('SKU inválido')
        if not inteiro(preco) or preco <= 0:
            raise ValueError('Preço inválido')
        if not inteiro(quantidade) or quantidade <= 0:
            raise ValueError('Quantidade inválida')
        solicitados[sku] = solicitados.get(sku, 0) + quantidade
        subtotal += preco * quantidade

    for sku, quantidade in solicitados.items():
        if quantidade > estoque[sku]:
            raise ValueError('Estoque insuficiente')

    desconto = subtotal * desconto_percentual // 100 if subtotal >= 10000 else 0
    frete = 0 if subtotal - desconto >= 15000 else 1500
    return {'subtotal_centavos': subtotal, 'desconto_centavos': desconto,
            'frete_centavos': frete, 'total_centavos': subtotal - desconto + frete}
