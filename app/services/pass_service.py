from app.models import db, User, Pass, Traveller
from datetime import datetime, timedelta

class PassService:
    @staticmethod
    def create_pass(user_id, data):
        """Create a new pass for a user"""
        user = User.query.get(user_id)
        if not user:
            raise Exception('User not found')
        
        if not data.get('traveller_name'):
            raise ValueError('Traveller name is required')
        
        # Create pass
        pass_obj = Pass(
            user_id=user_id,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.session.add(pass_obj)
        db.session.flush()  # Get the pass_id
        
        # Create traveller
        traveller = Traveller(
            pass_id=pass_obj.id,
            name=data['traveller_name'],
            created_at=datetime.utcnow()
        )
        db.session.add(traveller)
        
        db.session.commit()
        
        return {
            'pass_id': pass_obj.id,
            'traveller_id': traveller.id,
            'expires_at': pass_obj.expires_at.isoformat()
        }
    
    @staticmethod
    def get_all_passes(user_id):
        """Get all passes for a user"""
        user = User.query.get(user_id)
        if not user:
            raise Exception('User not found')
        
        passes = Pass.query.filter_by(user_id=user_id).all()
        result = []
        
        for pass_obj in passes:
            travellers = Traveller.query.filter_by(pass_id=pass_obj.id).all()
            result.append({
                'pass_id': pass_obj.id,
                'created_at': pass_obj.created_at.isoformat(),
                'expires_at': pass_obj.expires_at.isoformat(),
                'travellers': [{
                    'traveller_id': t.id,
                    'name': t.name,
                    'created_at': t.created_at.isoformat()
                } for t in travellers]
            })
        
        return {'passes': result}
    
    @staticmethod
    def delete_pass(user_id, pass_id):
        """Delete a pass and its associated travellers"""
        user = User.query.get(user_id)
        if not user:
            raise Exception('User not found')
        
        pass_obj = Pass.query.get(pass_id)
        if not pass_obj:
            raise Exception('Pass not found')
        
        if pass_obj.user_id != user_id:
            raise Exception('Pass does not belong to user')
        
        # Delete associated travellers
        Traveller.query.filter_by(pass_id=pass_id).delete()
        
        # Delete pass
        db.session.delete(pass_obj)
        db.session.commit() 