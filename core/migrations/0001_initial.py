# Generated by Django 4.0.5 on 2022-08-07 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssinaturaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_assinatura', models.ImageField(upload_to='uploads/assinatura/')),
            ],
        ),
        migrations.CreateModel(
            name='DisciplinaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
                ('descricao', models.TextField(blank=True, max_length=400, null=True)),
                ('data_inicio', models.DateField()),
                ('data_termino', models.DateField()),
                ('status', models.IntegerField(choices=[(1, 'Ativa'), (2, 'Inativa')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='EmailAdministrativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Email_Administrativo')], default=1, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('senha', models.CharField(max_length=6)),
                ('status', models.IntegerField(choices=[(1, 'ativo'), (2, 'desativado')], default=1)),
                ('permissao', models.IntegerField(choices=[(1, 'aluno'), (2, 'tutor'), (3, 'coordenador')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdminModel',
            fields=[
                ('usuariomodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.usuariomodel')),
            ],
            bases=('core.usuariomodel',),
        ),
        migrations.CreateModel(
            name='AlunoModel',
            fields=[
                ('usuariomodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.usuariomodel')),
                ('assinatura', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.assinaturamodel')),
            ],
            bases=('core.usuariomodel',),
        ),
        migrations.CreateModel(
            name='RelatorioModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.IntegerField(choices=[(1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')])),
                ('data_limite', models.DateField()),
                ('status', models.IntegerField(choices=[(1, 'aberto'), (2, 'fechado')], default=2)),
                ('disciplina', models.ManyToManyField(to='core.disciplinamodel')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.adminmodel')),
            ],
        ),
        migrations.CreateModel(
            name='CoordenadorModel',
            fields=[
                ('adminmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.adminmodel')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.adminmodel',),
        ),
        migrations.CreateModel(
            name='AvisoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('email_origem', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.emailadministrativo')),
                ('aluno', models.ManyToManyField(to='core.alunomodel')),
                ('usuario_remetente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.adminmodel')),
            ],
        ),
        migrations.CreateModel(
            name='TutorModel',
            fields=[
                ('adminmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.adminmodel')),
                ('assinatura', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.assinaturamodel')),
            ],
            bases=('core.adminmodel',),
        ),
        migrations.CreateModel(
            name='DocumentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_documento', models.CharField(max_length=200)),
                ('conteudo', models.TextField(unique=True)),
                ('disciplina', models.ManyToManyField(related_name='relatar_disciplina', to='core.disciplinamodel')),
                ('relatorio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.relatoriomodel')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.alunomodel')),
                ('tutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tutormodel')),
            ],
        ),
    ]
