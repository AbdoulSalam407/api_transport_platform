from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import Paiement, TransactionLog
from .serializers import PaiementSerializer, PaiementCreateSerializer, TransactionLogSerializer
from core.permissions import IsAdmin, IsPassager
import uuid


class PaiementViewSet(viewsets.ModelViewSet):
    """CRUD pour les paiements"""
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'admin':
            return Paiement.objects.all()
        else:
            return Paiement.objects.filter(utilisateur=user)


class TransactionLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Lecture des logs de transactions"""
    queryset = TransactionLog.objects.all()
    serializer_class = TransactionLogSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        queryset = TransactionLog.objects.all()
        paiement_id = self.request.query_params.get('paiement')
        if paiement_id:
            queryset = queryset.filter(paiement_id=paiement_id)
        return queryset


class InitierPaiementView(APIView):
    """Initier un paiement"""
    permission_classes = [IsPassager]
    
    @transaction.atomic
    def post(self, request):
        serializer = PaiementCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reservation = serializer.validated_data['reservation']
        
        # Vérifier que le passager est bien le propriétaire
        if reservation.passager.utilisateur != request.user:
            return Response(
                {'error': 'Vous n\'êtes pas autorisé à payer cette réservation'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Générer un ID de transaction unique
        transaction_id = str(uuid.uuid4()).replace('-', '')[:20]
        
        # Créer le paiement
        paiement = Paiement.objects.create(
            utilisateur=request.user,
            reservation=reservation,
            montant=serializer.validated_data['montant'],
            methode=serializer.validated_data['methode'],
            transaction_id=transaction_id,
            statut='en_cours'
        )
        
        # Créer un log
        TransactionLog.objects.create(
            paiement=paiement,
            action='initier',
            statut='en_cours',
            message='Paiement initié'
        )
        
        return Response(
            {
                'paiement': PaiementSerializer(paiement).data,
                'transaction_id': transaction_id
            },
            status=status.HTTP_201_CREATED
        )


class ConfirmerPaiementView(APIView):
    """Confirmer un paiement (callback API externe)"""
    permission_classes = [permissions.AllowAny]
    
    @transaction.atomic
    def post(self, request, transaction_id):
        try:
            paiement = Paiement.objects.get(transaction_id=transaction_id)
            
            statut = request.data.get('statut')
            reference = request.data.get('reference', '')
            
            if statut == 'success':
                paiement.valider()
                message = 'Paiement réussi'
            else:
                paiement.echouer()
                message = 'Paiement échoué'
            
            TransactionLog.objects.create(
                paiement=paiement,
                action='confirmer',
                statut='reussi' if statut == 'success' else 'echoue',
                message=message,
                data={'reference': reference, 'callback_data': request.data}
            )
            
            return Response({
                'message': message,
                'statut': paiement.statut
            })
            
        except Paiement.DoesNotExist:
            return Response(
                {'error': 'Transaction non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )


class VerifierPaiementView(APIView):
    """Vérifier le statut d'un paiement"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        try:
            paiement = Paiement.objects.get(id=pk)
            
            # Vérifier l'accès
            if request.user.role != 'admin' and paiement.utilisateur != request.user:
                return Response(
                    {'error': 'Accès non autorisé'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return Response(PaiementSerializer(paiement).data)
            
        except Paiement.DoesNotExist:
            return Response(
                {'error': 'Paiement non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


class RembourserPaiementView(APIView):
    """Rembourser un paiement"""
    permission_classes = [IsAdmin]
    
    @transaction.atomic
    def post(self, request, pk):
        try:
            paiement = Paiement.objects.get(id=pk)
            
            if paiement.statut != 'reussi':
                return Response(
                    {'error': 'Seul un paiement réussi peut être remboursé'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            paiement.rembourser()
            
            TransactionLog.objects.create(
                paiement=paiement,
                action='rembourser',
                statut='rembourse',
                message='Paiement remboursé'
            )
            
            return Response({
                'message': 'Paiement remboursé',
                'paiement': PaiementSerializer(paiement).data
            })
            
        except Paiement.DoesNotExist:
            return Response(
                {'error': 'Paiement non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )