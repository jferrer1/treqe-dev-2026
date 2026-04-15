# 🧩 Treqe Component Examples

**Ready-to-use React components for Treqe MVP**

---

## 1. Product Card Component

```tsx
// apps/web/components/ProductCard.tsx
import { Star, Heart, MessageCircle } from 'lucide-react';

interface ProductCardProps {
  product: {
    id: string;
    title: string;
    description: string;
    category: string;
    condition: 'new' | 'like_new' | 'good' | 'fair';
    images: string[];
    owner: {
      id: string;
      name: string;
      reputationScore: number;
      avatar?: string;
    };
    createdAt: Date;
  };
  onOfferClick?: (productId: string) => void;
  onSaveClick?: (productId: string) => void;
}

export default function ProductCard({ product, onOfferClick, onSaveClick }: ProductCardProps) {
  const conditionLabels = {
    new: 'Nuevo',
    like_new: 'Como nuevo',
    good: 'Buen estado',
    fair: 'Aceptable'
  };

  const getConditionColor = (condition: string) => {
    switch (condition) {
      case 'new': return 'bg-green-100 text-green-800';
      case 'like_new': return 'bg-blue-100 text-blue-800';
      case 'good': return 'bg-yellow-100 text-yellow-800';
      case 'fair': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="border border-gray-200 rounded-xl p-4 hover:shadow-lg transition-all duration-200 bg-white">
      {/* Product Image */}
      <div className="relative mb-4">
        <div className="aspect-square w-full bg-gray-100 rounded-lg overflow-hidden">
          {product.images[0] ? (
            <img 
              src={product.images[0]} 
              alt={product.title}
              className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400">
              <span>Sin imagen</span>
            </div>
          )}
        </div>
        
        {/* Save button */}
        <button
          onClick={() => onSaveClick?.(product.id)}
          className="absolute top-2 right-2 p-2 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-colors"
          aria-label="Guardar producto"
        >
          <Heart className="w-5 h-5 text-gray-600 hover:text-red-500" />
        </button>
      </div>

      {/* Product Details */}
      <div className="space-y-3">
        {/* Title and category */}
        <div>
          <h3 className="font-semibold text-lg text-gray-900 line-clamp-1">
            {product.title}
          </h3>
          <div className="flex items-center gap-2 mt-1">
            <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
              {product.category}
            </span>
            <span className={`px-2 py-1 text-xs rounded ${getConditionColor(product.condition)}`}>
              {conditionLabels[product.condition]}
            </span>
          </div>
        </div>

        {/* Description */}
        <p className="text-gray-600 text-sm line-clamp-2">
          {product.description}
        </p>

        {/* Owner info */}
        <div className="flex items-center justify-between pt-3 border-t border-gray-100">
          <div className="flex items-center gap-2">
            {/* Avatar */}
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-sm font-medium">
              {product.owner.avatar ? (
                <img src={product.owner.avatar} alt={product.owner.name} className="w-full h-full rounded-full" />
              ) : (
                product.owner.name.charAt(0).toUpperCase()
              )}
            </div>
            
            {/* Name and reputation */}
            <div>
              <p className="text-sm font-medium text-gray-900">{product.owner.name}</p>
              <div className="flex items-center gap-1">
                <Star className="w-3 h-3 text-yellow-500 fill-current" />
                <span className="text-xs text-gray-600">{product.owner.reputationScore}</span>
              </div>
            </div>
          </div>

          {/* Time ago */}
          <span className="text-xs text-gray-500">
            {formatTimeAgo(product.createdAt)}
          </span>
        </div>

        {/* Action buttons */}
        <div className="flex gap-2 pt-3">
          <button
            onClick={() => onOfferClick?.(product.id)}
            className="flex-1 px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-200 font-medium text-sm flex items-center justify-center gap-2"
          >
            <MessageCircle className="w-4 h-4" />
            Hacer oferta
          </button>
          
          <button
            onClick={() => onSaveClick?.(product.id)}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm"
          >
            Guardar
          </button>
        </div>
      </div>
    </div>
  );
}

// Helper function
function formatTimeAgo(date: Date): string {
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 60) return `${diffMins}m`;
  if (diffHours < 24) return `${diffHours}h`;
  if (diffDays < 7) return `${diffDays}d`;
  return `${Math.floor(diffDays / 7)}sem`;
}
```

---

## 2. Reputation Badge Component

```tsx
// apps/web/components/ReputationBadge.tsx
import { Star, TrendingUp, TrendingDown, Shield } from 'lucide-react';

interface ReputationBadgeProps {
  score: number;
  size?: 'sm' | 'md' | 'lg';
  showTrend?: boolean;
  trend?: 'up' | 'down' | 'neutral';
}

export default function ReputationBadge({ 
  score, 
  size = 'md', 
  showTrend = false,
  trend = 'neutral' 
}: ReputationBadgeProps) {
  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1.5',
    lg: 'text-base px-4 py-2'
  };

  const getReputationColor = (score: number) => {
    if (score >= 150) return 'bg-gradient-to-r from-green-500 to-emerald-600 text-white';
    if (score >= 120) return 'bg-gradient-to-r from-blue-500 to-cyan-600 text-white';
    if (score >= 90) return 'bg-gradient-to-r from-yellow-500 to-amber-600 text-white';
    if (score >= 60) return 'bg-gradient-to-r from-orange-500 to-red-500 text-white';
    return 'bg-gradient-to-r from-red-500 to-rose-600 text-white';
  };

  const getReputationLevel = (score: number) => {
    if (score >= 150) return { label: 'Excelente', icon: Shield };
    if (score >= 120) return { label: 'Muy bueno', icon: Star };
    if (score >= 90) return { label: 'Bueno', icon: Star };
    if (score >= 60) return { label: 'Regular', icon: Star };
    return { label: 'Nuevo', icon: Star };
  };

  const { label, icon: Icon } = getReputationLevel(score);
  const TrendIcon = trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : null;

  return (
    <div className={`inline-flex items-center gap-2 rounded-full ${sizeClasses[size]} ${getReputationColor(score)} font-medium`}>
      <Icon className="w-4 h-4" />
      <span className="font-bold">{score}</span>
      <span className="hidden sm:inline">{label}</span>
      
      {showTrend && TrendIcon && (
        <TrendIcon className={`w-4 h-4 ${trend === 'up' ? 'text-green-200' : 'text-red-200'}`} />
      )}
    </div>
  );
}
```

---

## 3. Offer Creation Modal

```tsx
// apps/web/components/OfferModal.tsx
'use client';

import { useState } from 'react';
import { X, Gift, DollarSign, Users, Send } from 'lucide-react';

interface OfferModalProps {
  isOpen: boolean;
  onClose: () => void;
  productId: string;
  productTitle: string;
  onSubmit: (offer: OfferData) => void;
}

interface OfferData {
  type: 'direct_swap' | 'cash_plus_product' | 'multi_party';
  message: string;
  offeredProductIds?: string[];
  cashAmount?: number;
  additionalParties?: string[];
}

export default function OfferModal({ 
  isOpen, 
  onClose, 
  productId, 
  productTitle,
  onSubmit 
}: OfferModalProps) {
  const [offerType, setOfferType] = useState<OfferData['type']>('direct_swap');
  const [message, setMessage] = useState('');
  const [cashAmount, setCashAmount] = useState('');
  const [selectedProducts, setSelectedProducts] = useState<string[]>([]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const offerData: OfferData = {
      type: offerType,
      message,
      offeredProductIds: offerType === 'direct_swap' ? selectedProducts : undefined,
      cashAmount: offerType === 'cash_plus_product' ? parseFloat(cashAmount) : undefined,
      additionalParties: offerType === 'multi_party' ? [] // Would come from UI
    };

    onSubmit(offerData);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl w-full max-w-md max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900">Crear oferta</h2>
              <p className="text-sm text-gray-600 mt-1">Para: {productTitle}</p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              aria-label="Cerrar"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Offer type selection */}
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-3">
              Tipo de oferta
            </label>
            <div className="grid grid-cols-3 gap-3">
              <button
                type="button"
                onClick={() => setOfferType('direct_swap')}
                className={`p-4 border rounded-xl flex flex-col items-center gap-2 transition-all ${
                  offerType === 'direct_swap' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <Gift className={`w-6 h-6 ${
                  offerType === 'direct_swap' ? 'text-blue-600' : 'text-gray-600'
                }`} />
                <span className="text-sm font-medium">Intercambio</span>
              </button>

              <button
                type="button"
                onClick={() => setOfferType('cash_plus_product')}
                className={`p-4 border rounded-xl flex flex-col items-center gap-2 transition-all ${
                  offerType === 'cash_plus_product' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <DollarSign className={`w-6 h-6 ${
                  offerType === 'cash_plus_product' ? 'text-blue-600' : 'text-gray-600'
                }`} />
                <span className="text-sm font-medium">Dinero + producto</span>
              </button>

              <button
                type="button"
                onClick={() => setOfferType('multi_party')}
                className={`p-4 border rounded-xl flex flex-col items-center gap-2 transition-all ${
                  offerType === 'multi_party' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <Users className={`w-6 h-6 ${
                  offerType === 'multi_party' ? 'text-blue-600' : 'text-gray-600'
                }`} />
                <span className="text-sm font-medium">Multiparte</span>
              </button>
            </div>
          </div>

          {/* Dynamic fields based on offer type */}
          {offerType === 'direct_swap' && (
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">
                Selecciona productos para intercambiar
              </label>
              <div className="space-y-2">
                {/* Product selection UI would go here */}
                <div className="p-4 border border-gray-200 rounded-lg text-center text-gray-500">
                  Lista de tus productos aparecerá aquí
                </div>
              </div>
            </div>
          )}

          {offerType === 'cash_plus_product' && (
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">
                Cantidad de dinero
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-500">€</span>
                </div>
                <input
                  type="number"
                  value={cashAmount}
                  onChange={(e) => setCashAmount(e.target.value)}
                  className="pl-8 w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="0.00"
                  min="0"
                  step="0.01"
                />
              </div>
            </div>
          )}

          {/* Message */}
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-2">
              Mensaje (opcional)
            </label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              rows={3}
              placeholder="Añade un mensaje personalizado para el vendedor..."
              maxLength={500}
            />
            <div className="text-right text-xs text-gray-500 mt-1">
              {message.length}/500 caracteres
            </div>
          </div>

          {/* Footer */}
          <div className="flex gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-200 font-medium flex items-center justify-center gap-2"
            >
              <Send className="w-4 h-4" />
              Enviar oferta
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

---

## 4. Matching Algorithm Visualization

```tsx
// apps/web/components/MatchingVisualization.tsx
'use client';

import { useEffect, useState } from 'react';
import { RefreshCw, Users, CheckCircle, XCircle } from 'lucide-react';

interface MatchingVisualizationProps {
  users: Array<{
    id: string;
    name: string;
    avatar?: string;
    product: string;
    wants: string;
  }>;
}

export default function MatchingVisualization({ users }: MatchingVisualizationProps) {
  const [matches, setMatches] = useState<Array<{from: string, to: string}>>([]);
  const [isAnimating, setIsAnimating] = useState(false);

  // Simulate k=3 matching algorithm
  const findMatches = () => {
    setIsAnimating(true);
    
    // Simple k=3 cycle detection
    const newMatches: Array<{from: string, to: string}> = [];
    
    // For demo: create a circular match between first 3 users
    if (users.length >= 3) {
      newMatches.push(
        { from: users[0].id, to: users[1].id },
        { from: users[1].id, to: users[2].id },
        {