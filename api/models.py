# import db from api module
import datetime
from api import db


# Define a base model for other database tables to inherit
class HyperParams(db.Model):
    __tablename__ = 'hyper_parameters'

    id = db.Column(db.Integer, primary_key=True)
    lr = db.Column(db.Float, nullable=False)
    epoch = db.Column(db.Integer, nullable=False)
    hidden_nodes = db.Column(db.Integer, nullable=False)
    model_name = db.Column(db.String(80), nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    graph_plot = db.relationship('ModelGraphData',
                                 back_populates='hyper_parameters',
                                 uselist=False, lazy='joined')

    def __repr__(self):
        return '<Model %r>' % self.model_name


class ModelGraphData(db.Model):
    __tablename__ = 'graph_plot'

    id = db.Column(db.Integer, primary_key=True)
    hyper_param_id = db.Column(db.Integer,
                               db.ForeignKey('hyper_parameters.id'),
                               nullable=False, unique=True)
    hyper_parameters = db.relationship('HyperParams',
                                       back_populates='graph_plot')
    lr_vs_p = db.Column(db.String(80), nullable=False)
    epoch_vs_p = db.Column(db.String(80), nullable=False)
    hn_vs_p = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return'<Model %r>' % self.id
