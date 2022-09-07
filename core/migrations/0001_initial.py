# Generated by Django 4.0.6 on 2022-09-07 00:26

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
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
            name='DocumentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_documento', models.FileField(upload_to='relatorios/')),
                ('disciplina', models.ManyToManyField(related_name='relatar_disciplina', to='core.disciplinamodel')),
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
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('permissao', models.IntegerField(choices=[(1, 'aluno'), (2, 'tutor'), (3, 'coordenador')])),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdminModel',
            fields=[
                ('usuariomodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.usuariomodel')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('core.usuariomodel',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AlunoModel',
            fields=[
                ('usuariomodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.usuariomodel')),
                ('assinatura', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.assinaturamodel')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('core.usuariomodel',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='RelatorioModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_relatorio', models.DateField(unique=True)),
                ('data_limite', models.DateField()),
                ('status', models.IntegerField(choices=[(1, 'aberto'), (2, 'fechado')], default=1)),
                ('disciplina', models.ManyToManyField(to='core.disciplinamodel')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.adminmodel')),
            ],
        ),
        migrations.CreateModel(
            name='RelatoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.documentmodel')),
            ],
        ),
        migrations.AddField(
            model_name='documentmodel',
            name='relatorio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.relatoriomodel'),
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
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='documentmodel',
            name='aluno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.alunomodel'),
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
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('core.adminmodel',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='documentmodel',
            name='tutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tutormodel'),
        ),
    ]
